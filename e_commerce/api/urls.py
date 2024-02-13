from django.urls import path, include
from e_commerce.product.views import (
    ProductView,
)

urlpatterns = [
    path('products/', ProductView.as_view()),
]