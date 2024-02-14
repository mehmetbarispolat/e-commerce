from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product
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
    def get(self, request, id):
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
