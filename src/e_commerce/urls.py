from django.urls import path

from .views import ProductView, ProductDetailView, ProductStockView

urlpatterns = [
    path("products/", ProductView.as_view()),
    path("products/<product_id>/", ProductDetailView.as_view()),
    path("products/<product_id>/stock/", ProductStockView.as_view()),
]
