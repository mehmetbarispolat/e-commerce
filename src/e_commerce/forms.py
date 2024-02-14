from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "product_type",
            "is_active",
            "stock_count",
            "price",
        ]
