from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductType(models.TextChoices):
    SINGLE = "single", _("Single")
    BUNDLE = "bundle", _("Bundle")


class SalesChannel(models.Model):
    TRENDYOL = "trendyol"
    HEPSIBURADA = "hepsiburada"
    SALES_CHANNEL_NAMES = [
        (TRENDYOL, "trendyol"),
        (HEPSIBURADA, "hepsiburada"),
    ]
    name = models.CharField(max_length=100, choices=SALES_CHANNEL_NAMES, unique=True)

    def __str__(self):
        return self.name


class ProductStock(models.Model):
    quantity = models.IntegerField(default=0)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    sales_channel = models.ForeignKey(
        SalesChannel, on_delete=models.CASCADE, related_name="products"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.CharField(
        max_length=20, choices=ProductType.choices, default=ProductType.SINGLE
    )
    bundled_products = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="bundles"
    )
    stock = models.ForeignKey(
        ProductStock, on_delete=models.CASCADE, related_name="stock"
    )
