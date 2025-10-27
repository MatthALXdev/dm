from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product


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


def purchase(request, slug):
    """Mock payment - redirect direct vers thanks"""
    if request.method == "POST":
        product = get_object_or_404(Product, slug=slug)
        # Mock payment - redirect direct vers thanks
        return redirect("thanks", slug=slug)
    return redirect("catalog")


def thanks(request, slug):
    """Page de remerciement après achat"""
    product = get_object_or_404(Product, slug=slug)
    return render(request, "core/thanks.html", {"product": product})