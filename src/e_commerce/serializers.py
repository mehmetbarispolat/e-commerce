from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
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
