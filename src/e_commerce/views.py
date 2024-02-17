from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Product, ProductStock
from .serializers import ProductSerializer


class ProductView(APIView):
    def get(self, request):
        products = Product.objects.all()
        if not products:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        stock_quantity = request.data.pop("stock_quantity", None)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Stok güncelleme işlemi
            if stock_quantity is not None:
                ProductStock.objects.update_or_create(
                    product=product, defaults={"quantity": stock_quantity}
                )

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
