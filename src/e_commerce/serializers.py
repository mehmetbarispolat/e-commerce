from rest_framework import serializers
from .models import Product, ProductStock


class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = ["quantity"]


class ProductSerializer(serializers.ModelSerializer):
    stock_quantity = serializers.IntegerField(write_only=True, required=False)
    stock = ProductStockSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "sales_channel",
            "price",
            "product_type",
            "bundled_products",
            "stock_quantity",
            "stock",
        ]

    def create(self, validated_data):
        stock_quantity = validated_data.pop("stock_quantity", 0)
        product = Product.objects.create(**validated_data)

        if product.product_type == Product.SINGLE:
            ProductStock.objects.create(product=product, quantity=stock_quantity)
        elif product.product_type == Product.BUNDLE:
            min_stock = min(
                [p.stock.quantity for p in product.bundled_products.all()], default=0
            )
            ProductStock.objects.create(product=product, quantity=min_stock)

        return product
