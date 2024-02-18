from django.core.exceptions import ValidationError
from django.http import Http404
from django.db import transaction
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


class BundleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name",)


class ProductSerializer(serializers.ModelSerializer):
    stock_quantity = serializers.IntegerField(write_only=True, required=False)
    sales_channel_name = serializers.ChoiceField(
        choices=SalesChannel.SALES_CHANNEL_NAMES, write_only=True, required=True
    )
    bundled_product_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=0), write_only=True, required=False
    )
    stock = ProductStockSerializer(read_only=True)
    sales_channel = SalesChannelSerializer(read_only=True)
    bundled_products = BundleProductSerializer(many=True, read_only=True)

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
            "bundled_product_ids",
            "stock_quantity",
            "stock",
            "sales_channel_name",
        ]

    @transaction.atomic
    def create(self, validated_data: dict):
        bundled_products_ids: list[int] = validated_data.pop("bundled_product_ids", [])
        stock_quantity: int = validated_data.pop("stock_quantity", 0)
        sales_channel_name: str = validated_data.pop("sales_channel_name", "")
        sales_channel, _ = SalesChannel.objects.get_or_create(name=sales_channel_name)

        # TODO: Write as declarative
        product = Product(**validated_data, sales_channel=sales_channel)

        try:
            # TODO: Add SKU into product because name is not unique
            product_from_different_channel = Product.objects.get(
                name=validated_data.get("name")
            )
            if product_from_different_channel.stock.quantity != stock_quantity:
                raise ValidationError(
                    "Stock quatity of product must be same for each sales channel."
                )
            product.stock = ProductStock.objects.get(
                id=product_from_different_channel.stock.id
            )

        except Product.DoesNotExist:
            if product.product_type == ProductType.BUNDLE:
                if not bundled_products_ids:
                    raise ValidationError(
                        "bundled_product_ids field is required for Bundle product"
                    )
                # product.save() çağrısını product.bundled_products.set(bundled_products) satırından önce yapmanız gerekmektedir,
                # ancak product nesnesinin stock ilişkisi de bir ForeignKey olduğu için ve bu stock nesnesi product kaydedilmeden önce oluşturulup kaydedilmeli.
                # Bu nedenle, product nesnesinin ManyToManyField ilişkisini ayarlamadan önce hem product nesnesini
                # hem de gerekli stock nesnesini kaydetmek için doğru sıralamayı yapmanız gerekiyor.
                product.save()
                # Process bundled products
                bundled_products = Product.objects.filter(id__in=bundled_products_ids)
                if not all(
                    bp.sales_channel == sales_channel for bp in bundled_products
                ):
                    raise ValidationError(
                        "All bundled products must be from the same sales channel."
                    )

                # Set the bundled_products ManyToMany field
                product.bundled_products.set(bundled_products)

                # Set the stock quantity to the minimum stock quantity of included products
                min_stock_product = min(
                    bundled_products, key=lambda bp: bp.stock.quantity
                )
                product.stock = min_stock_product.stock
            elif product.product_type == ProductType.SINGLE:
                # Create stock for SINGLE product type
                product.stock = ProductStock.objects.create(quantity=stock_quantity)

        product.save()

        return product

    @transaction.atomic
    def update(self, instance: Product, validated_data: dict):
        sales_channel_name: str = validated_data.pop("sales_channel_name", "")
        sales_channel, _ = SalesChannel.objects.get_or_create(name=sales_channel_name)

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)

        # Update stock quantity
        stock_quantity = validated_data.pop("stock_quantity", None)
        if stock_quantity is not None:
            # If the instance does not have an associated stock object, create a new one
            if not instance.stock:
                instance.stock = ProductStock.objects.create(quantity=stock_quantity)
            else:
                # Update the quantity of the existing stock object
                instance.stock.quantity = stock_quantity
                # Save the updated stock object
                instance.stock.save()

        instance.sales_channel = sales_channel
        instance.save()

        # The update for bundled products can be performed here.
        bundled_product_ids = validated_data.get("bundled_product_ids", [])
        if bundled_product_ids:
            instance.bundled_products.set(bundled_product_ids)

        return instance
