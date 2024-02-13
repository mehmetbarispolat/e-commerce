from rest_framework import viewsets
from e_commerce.product.models import Product
from e_commerce.product.serializers import ProductSerializer


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
