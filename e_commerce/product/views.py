from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from e_commerce.product.models import Product
from e_commerce.product.serializers import ProductSerializer


# Create your views here.
class ProductView(APIView):

    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        products = Product.objects.filter(user = request.user.id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
