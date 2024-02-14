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
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
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
