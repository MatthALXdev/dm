from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Product, Order
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


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
                success_url=request.build_absolute_uri(f'/thanks/?session_id={{CHECKOUT_SESSION_ID}}'),
                cancel_url=request.build_absolute_uri(f'/product/{product.slug}/'),
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
        return redirect('catalog')

    try:
        # Récupérer la session Stripe
        checkout_session = stripe.checkout.Session.retrieve(session_id)

        context = {
            'session_id': session_id,
            'payment_status': checkout_session.payment_status,
            'amount_total': checkout_session.amount_total / 100,  # Convertir centimes en euros
            'customer_email': checkout_session.customer_details.email if checkout_session.customer_details else None,
        }

        return render(request, "core/thanks.html", context)

    except stripe.error.StripeError:
        return redirect('catalog')