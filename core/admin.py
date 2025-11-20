from django.contrib import admin
from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "amount", "status", "stripe_session_id", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("stripe_session_id", "product__name")
    readonly_fields = ("created_at", "updated_at")
