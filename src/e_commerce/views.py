from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, ProductStock
from .serializers import ProductSerializer


# Create your views here.
class ProductView(APIView):
    """
    List all products, or create a new product.
    """

    def get(self, request, format=None):
        """List all products"""
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """Create products
        body:
            [
                {
                    "name": "Logitech Klavye",
                    "description": "Klavye",
                    "product_type": "Single",
                    "stock_count": 5,
                    "price": 1050
                }
            ]

        """
        # TODO: Add control to check whether incoming product is bundle product or not.
        serializer = ProductSerializer(data=request.data, many=True)
        if serializer.is_valid():
            Product.objects.bulk_create(
                *[
                    map(
                        lambda product_obj: Product(**product_obj),
                        serializer.data,
                    )
                ]
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.select_related("stock").get(id=product_id)
        except Product.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        # TODO: Add response Serializer
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, product_id):
        # TODO: Add partial update. Fix KeyError
        serializer = ProductSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            Product.objects.filter(id=product_id).update(**serializer.data)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product_to_delete = Product.objects.filter(id=product_id)
        if not product_to_delete:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        product_to_delete.delete()
        return Response({"message": "Deleted successfully"}, status.HTTP_200_OK)


class ProductStockView(APIView):
    def post(self, request, product_id):
        # TODO: Add request serializer
        stock = ProductStock.objects.create(count=request.data["count"])
        Product.objects.filter(id=product_id).update(stock_count=stock)

        return Response(request.data, status=status.HTTP_200_OK)
