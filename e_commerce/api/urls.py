from django.urls import path
from rest_framework import routers

from e_commerce.product.views import ProductViewSet


router = routers.DefaultRouter()
router.register(r"^products", ProductViewSet)
