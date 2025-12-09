from django.urls import path
from .views import (
    health, hello, home, root, catalog_view, product_view,
    checkout, thanks, stripe_webhook, download_view
)

urlpatterns = [
    path("", root, name="root"),
    path("home/", home, name="home"),
    path("health", health, name="health"),
    path("hello", hello, name="hello"),
    path("catalog/", catalog_view, name="catalog"),
    path("product/<slug:slug>/", product_view, name="product"),
    path("checkout/<slug:slug>/", checkout, name="checkout"),
    path("thanks/", thanks, name="thanks"),
    path("webhook/", stripe_webhook, name="stripe_webhook"),
    path("download/<str:token>/", download_view, name="download"),
]