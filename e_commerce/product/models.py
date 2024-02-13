from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=200)

    def __str__(self):
        return self.sku

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
