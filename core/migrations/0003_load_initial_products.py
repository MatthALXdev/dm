# Generated manually for initial product data

from django.db import migrations


def load_initial_products(apps, schema_editor):
    """
    Charge les 3 produits initiaux en production.
    Note: Les images doivent être placées manuellement dans media/products/
    """
    Product = apps.get_model('core', 'Product')

    products_data = [
        {
            'name': 'Pack Nature',
            'slug': 'pack-nature',
            'description': '10 magnifiques fonds d\'écran nature en haute définition',
            'price': '9.99',
            'image': 'products/forest_path.png'
        },
        {
            'name': 'Pack Abstract',
            'slug': 'pack-abstract',
            'description': '15 fonds d\'écran abstraits et colorés',
            'price': '14.99',
            'image': 'products/ocean_waves.png'
        },
        {
            'name': 'Pack Minimal',
            'slug': 'pack-minimal',
            'description': '20 fonds d\'écran minimalistes et élégants',
            'price': '19.99',
            'image': 'products/montain_sunset.png'
        }
    ]

    for data in products_data:
        Product.objects.get_or_create(
            slug=data['slug'],
            defaults={
                'name': data['name'],
                'description': data['description'],
                'price': data['price'],
                'image': data['image']
            }
        )


def remove_products(apps, schema_editor):
    """Rollback: supprime les produits si on revient en arrière"""
    Product = apps.get_model('core', 'Product')
    Product.objects.filter(slug__in=['pack-nature', 'pack-abstract', 'pack-minimal']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_product_image'),
    ]

    operations = [
        migrations.RunPython(load_initial_products, remove_products),
    ]
