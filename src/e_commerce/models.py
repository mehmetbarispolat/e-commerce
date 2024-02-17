from django.db import models


class Product(models.Model):
    SINGLE = "single"
    BUNDLE = "bundle"
    PRODUCT_TYPE_CHOICES = [
        (SINGLE, "Single"),
        (BUNDLE, "Bundle"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    sales_channel = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.CharField(
        max_length=10, choices=PRODUCT_TYPE_CHOICES, default=SINGLE
    )
    bundled_products = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="bundles"
    )


class ProductStock(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="stock"
    )
    quantity = models.IntegerField(default=0)
