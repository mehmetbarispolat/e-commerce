from django.urls import path
from .views import ProductView, ProductDetail

urlpatterns = [
    path("products/", ProductView.as_view(), name="product"),
    path("products/<int:pk>/", ProductDetail.as_view(), name="product-detail"),
]
