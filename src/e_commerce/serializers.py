from django.http import Http404
from rest_framework import serializers

from .models import Product, ProductStock, SalesChannel, ProductType


class SalesChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesChannel
        fields = ["id", "name"]


class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = ["id", "quantity"]


class ProductSerializer(serializers.ModelSerializer):
    stock_quantity = serializers.IntegerField(write_only=True, required=False)
    sales_channel_name = serializers.ChoiceField(
        choices=SalesChannel.SALES_CHANNEL_NAMES, write_only=True, required=True
    )
    stock = ProductStockSerializer(read_only=True)
    sales_channel = SalesChannelSerializer(read_only=True)

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
            "sales_channel_name",
        ]

    def create(self, validated_data: dict):
        stock_quantity: int = validated_data.pop("stock_quantity", 0)
        sales_channel_name: str = validated_data.pop("sales_channel_name", "")
        sales_channel, _ = SalesChannel.objects.get_or_create(name=sales_channel_name)

        # TODO: Write as declarative
        product = Product(**{**validated_data, "sales_channel": sales_channel})

        # TODO: Add same product_id for trendyol, hepsiburada into stock
        try:
            # Trendyol 3 geldi hepsiburada 3
            # TODO: Add SKU into product because name is not unique
            product_from_different_channel = Product.objects.get(
                name=validated_data.get("name")
            )
            if product_from_different_channel.stock.quantity != stock_quantity:
                # TODO: Add specific exception handler
                raise Http404
            product.stock = ProductStock.objects.get(
                id=product_from_different_channel.stock.id
            )
        except Product.DoesNotExist:
            if product.product_type == ProductType.SINGLE:
                product.stock = ProductStock.objects.create(quantity=stock_quantity)
            elif product.product_type == ProductType.BUNDLE:
                min_stock = min(
                    [p.stock.quantity for p in product.bundled_products.all()],
                    default=0,
                )
                product.stock = ProductStock.objects.create(quantity=min_stock)

        product.save()

        return product
