from django.db import models

PRODUCT_TYPE = (("Single", "Single"), ("Bundle", "Bundle"))


class ProductStock(models.Model):
    count = models.PositiveSmallIntegerField(verbose_name="Stock Count", default=0)

    class Meta:
        db_table = "stock"

    def __str__(self) -> str:
        return self.count


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Product Name")
    description = models.TextField(verbose_name="Description", max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE, null=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    stock = models.OneToOneField(
        ProductStock,
        related_name="stock",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    price = models.DecimalField(verbose_name="Price", decimal_places=2, max_digits=10)

    class Meta:
        db_table = "products"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name


# class SalesChannel(models.Model):
