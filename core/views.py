from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Order
import stripe
import logging

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


def health(request):
    return JsonResponse({"status": "ok"})


def hello(request):
    return HttpResponse("Hello World 🚀")


def home(request):
    return render(request, "core/home.html")


def root(request):
    return redirect("home")


def catalog_view(request):
    products = Product.objects.all()
    return render(request, "core/catalog.html", {"products": products})


def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "core/product.html", {"product": product})


def checkout(request, slug):
    """Créer Stripe Checkout Session et rediriger vers Stripe"""
    if request.method == "POST":
        product = get_object_or_404(Product, slug=slug)

        try:
            # Construire l'URL de base dynamiquement (dev/prod)
            base_url = f"{request.scheme}://{request.get_host()}"
            success_url = f'{base_url}/thanks/?session_id={{CHECKOUT_SESSION_ID}}'

            # Créer Stripe Checkout Session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': product.name,
                            'description': product.description,
                        },
                        'unit_amount': int(product.price * 100),  # Convertir en centimes
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=f'{base_url}/product/{product.slug}/',
                metadata={
                    'product_id': product.id,
                },
            )

            # Rediriger vers Stripe hosted checkout page
            return redirect(checkout_session.url)

        except stripe.error.StripeError as e:
            # En cas d'erreur Stripe, retourner à la page produit
            return redirect('product', slug=slug)

    return redirect("catalog")


def thanks(request):
    """Page de remerciement après achat"""
    session_id = request.GET.get('session_id')

    if not session_id:
        messages.warning(request, "Aucune session de paiement trouvée.")
        return redirect('catalog')

    try:
        checkout_session = stripe.checkout.Session.retrieve(session_id)

        if checkout_session.status == 'expired':
            messages.error(request, "Cette session de paiement a expiré (>24h). Veuillez recommencer votre achat.")
            logger.warning(f"Session expirée: {session_id}")
            return redirect('catalog')

        # Récupérer l'Order si disponible (créé par webhook)
        order = None
        try:
            order = Order.objects.get(stripe_session_id=session_id)
        except Order.DoesNotExist:
            # Fallback: Si webhook n'a pas créé l'Order, le créer maintenant
            # Cela permet de fonctionner en dev local sans Stripe CLI
            if checkout_session.payment_status == 'paid':
                product_id = checkout_session.metadata.get('product_id')
                if product_id:
                    try:
                        product = Product.objects.get(id=product_id)
                        order = Order.objects.create(
                            product=product,
                            stripe_session_id=session_id,
                            email=checkout_session.customer_details.email,
                            amount=checkout_session.amount_total / 100,
                            status='paid',
                        )
                        logger.info(f"Order #{order.id} créé via fallback (webhook non reçu): {order.email} - {product.name}")
                    except Product.DoesNotExist:
                        logger.error(f"Product {product_id} introuvable pour session {session_id}")
                else:
                    logger.warning(f"Metadata product_id manquant pour session {session_id}")

        context = {
            'session_id': session_id,
            'payment_status': checkout_session.payment_status,
            'amount_total': checkout_session.amount_total / 100,
            'customer_email': checkout_session.customer_details.email if checkout_session.customer_details else None,
            'order': order,
        }

        return render(request, "core/thanks.html", context)

    except stripe.error.InvalidRequestError as e:
        messages.error(request, "Session de paiement invalide ou expirée.")
        logger.error(f"Session invalide {session_id}: {str(e)}")
        return redirect('catalog')
    except stripe.error.StripeError as e:
        messages.error(request, "Erreur lors de la récupération du paiement.")
        logger.error(f"Erreur Stripe pour session {session_id}: {str(e)}")
        return redirect('catalog')


@csrf_exempt
def stripe_webhook(request):
    """Webhook Stripe pour confirmer les paiements"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    if not webhook_secret:
        logger.error("STRIPE_WEBHOOK_SECRET non configuré")
        return HttpResponse(status=500)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        logger.error("Webhook: Payload invalide")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        logger.error("Webhook: Signature invalide")
        return HttpResponse(status=400)

    # Gérer l'événement checkout.session.completed
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session_completed(session)

    return HttpResponse(status=200)


def handle_checkout_session_completed(session):
    """Créer Order après paiement confirmé"""
    session_id = session['id']
    product_id = session['metadata'].get('product_id')

    if not product_id:
        logger.error(f"Webhook: product_id manquant pour session {session_id}")
        return

    try:
        product = Product.objects.get(id=product_id)

        # Éviter les doublons (webhook peut être envoyé plusieurs fois)
        if Order.objects.filter(stripe_session_id=session_id).exists():
            logger.info(f"Order déjà existant pour session {session_id}")
            return

        # Créer l'Order
        order = Order.objects.create(
            product=product,
            stripe_session_id=session_id,
            email=session['customer_details']['email'],
            amount=session['amount_total'] / 100,
            status='paid',
        )

        logger.info(f"Order #{order.id} créé: {order.email} - {product.name} - Token: {order.download_token}")

    except Product.DoesNotExist:
        logger.error(f"Webhook: Product {product_id} introuvable pour session {session_id}")
    except Exception as e:
        logger.error(f"Webhook: Erreur lors de la création Order pour session {session_id}: {str(e)}")


def download_view(request, token):
    """Page de téléchargement avec vérification du token"""
    try:
        order = Order.objects.get(download_token=token, status='paid')
    except Order.DoesNotExist:
        messages.error(request, "Token de téléchargement invalide ou expiré.")
        return redirect('catalog')

    # Incrémenter le compteur de téléchargements
    order.download_count += 1
    order.save()

    # Récupérer le fichier produit
    if not order.product.image:
        messages.error(request, "Fichier non disponible pour ce produit.")
        logger.error(f"Fichier manquant pour Order #{order.id} - Product #{order.product.id}")
        return redirect('catalog')

    context = {
        'order': order,
        'product': order.product,
        'download_url': order.product.image.url,
    }

    return render(request, "core/download.html", context)