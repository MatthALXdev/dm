from django.urls import path
from .views import health, hello, home, root, catalog_view, product_view

urlpatterns = [
    path("", root, name="root"),
    path("home/", home, name="home"),
    path("health", health, name="health"),
    path("hello", hello, name="hello"),
    path("catalog/", catalog_view, name="catalog"),
    path("product/<slug:slug>/", product_view, name="product"),
]