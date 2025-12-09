from django.db import models
import secrets


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orders')
    stripe_session_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(default='')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    download_token = models.CharField(max_length=64, unique=True, db_index=True, default='')
    download_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.product.name} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.download_token:
            self.download_token = secrets.token_urlsafe(48)
        super().save(*args, **kwargs)
