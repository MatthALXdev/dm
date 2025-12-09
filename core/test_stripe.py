import pytest
from django.test import Client
from django.contrib.messages import get_messages
from unittest.mock import patch, MagicMock
from core.models import Product, Order
from decimal import Decimal
import json
import hmac
import hashlib
import time


@pytest.mark.django_db
class TestStripeCheckout:
    def test_checkout_creates_session_and_redirects(self):
        """POST /checkout/ crée session Stripe et redirige"""
        product = Product.objects.create(name="Test", slug="test", price=9.99)

        with patch('stripe.checkout.Session.create') as mock_create:
            mock_create.return_value = MagicMock(url='https://checkout.stripe.com/test')

            client = Client()
            response = client.post(f'/checkout/{product.slug}/')

            assert response.status_code == 302
            assert 'checkout.stripe.com' in response.url
            mock_create.assert_called_once()

    def test_checkout_invalid_slug_returns_404(self):
        """POST /checkout/ avec slug invalide → 404"""
        client = Client()
        response = client.post('/checkout/invalid-slug/')
        assert response.status_code == 404

    def test_checkout_get_method_redirects(self):
        """GET /checkout/ redirige vers catalogue"""
        product = Product.objects.create(name="Test", slug="test", price=9.99)
        client = Client()
        response = client.get(f'/checkout/{product.slug}/')
        assert response.status_code == 302
        assert response.url == '/catalog/'


@pytest.mark.django_db
class TestThanksPage:
    def test_thanks_with_valid_session(self):
        """/thanks/ avec session valide affiche données"""
        with patch('stripe.checkout.Session.retrieve') as mock_retrieve:
            mock_retrieve.return_value = MagicMock(
                status='complete',
                payment_status='paid',
                amount_total=999,
                customer_details=MagicMock(email='test@example.com')
            )

            client = Client()
            response = client.get('/thanks/?session_id=cs_test_123')

            assert response.status_code == 200
            content = response.content.decode('utf-8')
            assert 'test@example.com' in content
            assert 'Merci pour votre achat' in content

    def test_thanks_without_session_id_redirects(self):
        """/thanks/ sans session_id redirige avec message"""
        client = Client()
        response = client.get('/thanks/', follow=True)

        assert response.status_code == 200
        assert response.redirect_chain[-1][0] == '/catalog/'
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert 'Aucune session' in str(messages[0])

    def test_thanks_with_expired_session(self):
        """/thanks/ avec session expirée redirige avec message"""
        with patch('stripe.checkout.Session.retrieve') as mock_retrieve:
            mock_retrieve.return_value = MagicMock(status='expired')

            client = Client()
            response = client.get('/thanks/?session_id=cs_test_exp', follow=True)

            assert response.redirect_chain[-1][0] == '/catalog/'
            messages = list(get_messages(response.wsgi_request))
            assert any('expiré' in str(m) for m in messages)

    def test_thanks_with_invalid_session(self):
        """/thanks/ avec session invalide redirige avec message"""
        with patch('stripe.checkout.Session.retrieve') as mock_retrieve:
            from stripe.error import InvalidRequestError
            mock_retrieve.side_effect = InvalidRequestError('Invalid', param='id')

            client = Client()
            response = client.get('/thanks/?session_id=cs_test_inv', follow=True)

            assert response.redirect_chain[-1][0] == '/catalog/'
            messages = list(get_messages(response.wsgi_request))
            assert any('invalide' in str(m) for m in messages)


@pytest.mark.django_db
class TestSecurity:
    def test_sql_injection_in_slug(self):
        """Protection injection SQL via slug"""
        client = Client()
        response = client.get("/product/test'; DROP TABLE products;--/")
        assert response.status_code == 404

    def test_xss_in_product_name(self):
        """Protection XSS dans product.name"""
        product = Product.objects.create(
            name="<script>alert('XSS')</script>",
            slug="xss-test",
            price=9.99
        )

        client = Client()
        response = client.get(f'/product/{product.slug}/')

        assert b'<script>' not in response.content
        assert b'&lt;script&gt;' in response.content

    def test_csrf_protection_on_checkout(self):
        """Protection CSRF sur POST /checkout/"""
        product = Product.objects.create(name="Test", slug="test", price=9.99)
        client = Client(enforce_csrf_checks=True)

        response = client.post(f'/checkout/{product.slug}/')
        assert response.status_code == 403

    def test_price_from_database_not_client(self):
        """Prix vient de la DB (pas modifiable par client)"""
        product = Product.objects.create(name="Test", slug="test", price=99.99)

        with patch('stripe.checkout.Session.create') as mock_create:
            mock_create.return_value = MagicMock(url='https://checkout.stripe.com/test')

            client = Client()
            client.post(f'/checkout/{product.slug}/')

            call_kwargs = mock_create.call_args[1]
            unit_amount = call_kwargs['line_items'][0]['price_data']['unit_amount']
            assert unit_amount == 9999


@pytest.mark.django_db
class TestWebhook:
    def generate_signature(self, payload, secret):
        """Générer signature Stripe valide pour tests"""
        timestamp = int(time.time())
        payload_str = payload if isinstance(payload, str) else json.dumps(payload)
        signed_payload = f"{timestamp}.{payload_str}"
        signature = hmac.new(
            secret.encode('utf-8'),
            signed_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return f"t={timestamp},v1={signature}"

    def test_webhook_creates_order(self):
        """Webhook crée Order après checkout.session.completed"""
        product = Product.objects.create(name="Test", slug="test", price=9.99)

        event_data = {
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'id': 'cs_test_webhook_123',
                    'metadata': {'product_id': str(product.id)},
                    'customer_details': {'email': 'webhook@example.com'},
                    'amount_total': 999,
                    'payment_status': 'paid'
                }
            }
        }

        with patch('stripe.Webhook.construct_event') as mock_construct:
            mock_construct.return_value = event_data

            client = Client()
            response = client.post(
                '/webhook/',
                data=json.dumps(event_data),
                content_type='application/json',
                HTTP_STRIPE_SIGNATURE='fake_signature'
            )

            assert response.status_code == 200
            assert Order.objects.filter(stripe_session_id='cs_test_webhook_123').exists()

            order = Order.objects.get(stripe_session_id='cs_test_webhook_123')
            assert order.email == 'webhook@example.com'
            assert order.amount == Decimal('9.99')
            assert order.status == 'paid'
            assert len(order.download_token) > 0

    def test_webhook_invalid_signature(self):
        """Webhook rejette signature invalide"""
        with patch('stripe.Webhook.construct_event') as mock_construct:
            from stripe.error import SignatureVerificationError
            mock_construct.side_effect = SignatureVerificationError('Invalid', 'sig')

            client = Client()
            response = client.post(
                '/webhook/',
                data='{}',
                content_type='application/json',
                HTTP_STRIPE_SIGNATURE='invalid_signature'
            )

            assert response.status_code == 400

    def test_webhook_duplicate_prevention(self):
        """Webhook ne crée pas de doublon si Order existe déjà"""
        product = Product.objects.create(name="Test", slug="test", price=9.99)
        Order.objects.create(
            product=product,
            stripe_session_id='cs_test_duplicate',
            email='first@example.com',
            amount=9.99,
            status='paid'
        )

        event_data = {
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'id': 'cs_test_duplicate',
                    'metadata': {'product_id': str(product.id)},
                    'customer_details': {'email': 'second@example.com'},
                    'amount_total': 999,
                }
            }
        }

        with patch('stripe.Webhook.construct_event') as mock_construct:
            mock_construct.return_value = event_data

            client = Client()
            response = client.post(
                '/webhook/',
                data=json.dumps(event_data),
                content_type='application/json',
                HTTP_STRIPE_SIGNATURE='fake_signature'
            )

            assert response.status_code == 200
            assert Order.objects.filter(stripe_session_id='cs_test_duplicate').count() == 1
            order = Order.objects.get(stripe_session_id='cs_test_duplicate')
            assert order.email == 'first@example.com'

    def test_webhook_missing_product_id(self):
        """Webhook gère metadata sans product_id"""
        event_data = {
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'id': 'cs_test_no_product',
                    'metadata': {},
                    'customer_details': {'email': 'test@example.com'},
                    'amount_total': 999,
                }
            }
        }

        with patch('stripe.Webhook.construct_event') as mock_construct:
            mock_construct.return_value = event_data

            client = Client()
            response = client.post(
                '/webhook/',
                data=json.dumps(event_data),
                content_type='application/json',
                HTTP_STRIPE_SIGNATURE='fake_signature'
            )

            assert response.status_code == 200
            assert not Order.objects.filter(stripe_session_id='cs_test_no_product').exists()


@pytest.mark.django_db
class TestDownload:
    def test_download_with_valid_token(self):
        """Téléchargement avec token valide affiche page"""
        from django.core.files.uploadedfile import SimpleUploadedFile

        product = Product.objects.create(
            name="Test",
            slug="test",
            price=9.99,
            image=SimpleUploadedFile("test.jpg", b"fake_image_content", content_type="image/jpeg")
        )
        order = Order.objects.create(
            product=product,
            stripe_session_id='cs_test_download',
            email='download@example.com',
            amount=9.99,
            status='paid'
        )

        client = Client()
        response = client.get(f'/download/{order.download_token}/')

        assert response.status_code == 200
        assert b'download@example.com' in response.content
        assert b'Test' in response.content

        order.refresh_from_db()
        assert order.download_count == 1

    def test_download_increments_counter(self):
        """Compteur téléchargement s'incrémente"""
        from django.core.files.uploadedfile import SimpleUploadedFile

        product = Product.objects.create(
            name="Test",
            slug="test",
            price=9.99,
            image=SimpleUploadedFile("test.jpg", b"fake_image_content", content_type="image/jpeg")
        )
        order = Order.objects.create(
            product=product,
            stripe_session_id='cs_test_counter',
            email='counter@example.com',
            amount=9.99,
            status='paid'
        )

        client = Client()
        client.get(f'/download/{order.download_token}/')
        client.get(f'/download/{order.download_token}/')
        client.get(f'/download/{order.download_token}/')

        order.refresh_from_db()
        assert order.download_count == 3

    def test_download_with_invalid_token(self):
        """Token invalide redirige avec message"""
        client = Client()
        response = client.get('/download/invalid_token_123/', follow=True)

        assert response.status_code == 200
        assert response.redirect_chain[-1][0] == '/catalog/'
        messages = list(get_messages(response.wsgi_request))
        assert any('invalide' in str(m) for m in messages)

    def test_download_requires_paid_status(self):
        """Seuls les orders 'paid' permettent téléchargement"""
        product = Product.objects.create(name="Test", slug="test", price=9.99)
        order = Order.objects.create(
            product=product,
            stripe_session_id='cs_test_pending',
            email='pending@example.com',
            amount=9.99,
            status='pending'
        )

        client = Client()
        response = client.get(f'/download/{order.download_token}/', follow=True)

        assert response.redirect_chain[-1][0] == '/catalog/'
        messages = list(get_messages(response.wsgi_request))
        assert any('invalide' in str(m) for m in messages)