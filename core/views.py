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