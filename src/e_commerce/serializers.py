from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "created_at",
            "description",
            "product_type",
            "is_active",
            "stock",
            "price",
        ]
