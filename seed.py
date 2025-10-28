#!/usr/bin/env python
"""
Script de seed pour charger les produits avec leurs images
"""
import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.files import File
from core.models import Product

def seed_products():
    """Charge les produits avec leurs images"""
    
    # Supprimer les produits existants
    Product.objects.all().delete()
    print("✓ Produits existants supprimés")
    
    # Définir les produits
    products_data = [
        {
            "name": "Pack Nature",
            "slug": "pack-nature",
            "description": "10 magnifiques fonds d'écran nature en haute définition",
            "price": "9.99",
            "image_path": "core/fixtures/img/forest_path.png"
        },
        {
            "name": "Pack Abstract",
            "slug": "pack-abstract",
            "description": "15 fonds d'écran abstraits et colorés",
            "price": "14.99",
            "image_path": "core/fixtures/img/ocean_waves.png"
        },
        {
            "name": "Pack Minimal",
            "slug": "pack-minimal",
            "description": "20 fonds d'écran minimalistes et élégants",
            "price": "19.99",
            "image_path": "core/fixtures/img/montain_sunset.png"
        }
    ]
    
    # Créer les produits
    for data in products_data:
        image_path = Path(data.pop('image_path'))
        
        if image_path.exists():
            with open(image_path, 'rb') as img_file:
                product = Product(
                    name=data['name'],
                    slug=data['slug'],
                    description=data['description'],
                    price=data['price']
                )
                product.image.save(image_path.name, File(img_file), save=True)
                print(f"✓ Produit créé: {product.name} avec image {image_path.name}")
        else:
            print(f"✗ Image non trouvée: {image_path}")
    
    print(f"\n✓ {Product.objects.count()} produits chargés avec succès!")

if __name__ == '__main__':
    seed_products()
