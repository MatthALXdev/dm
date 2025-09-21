from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect


def health(request):
    return JsonResponse({"status": "ok"})


def hello(request):
    return HttpResponse("Hello World 🚀")


def home(request):
    return render(request, "core/home.html")


def root(request):
    return redirect("home")