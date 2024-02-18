from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, SalesChannel, ProductStock


class ProductTests(APITestCase):
    def setUp(self):
        # Create predefined SalesChannel and ProductStock
        self.sales_channel = SalesChannel.objects.create(name=SalesChannel.TRENDYOL)
        self.product_stock = ProductStock.objects.create(quantity=100)

    def test_create_product(self):
        """
        Tests product creation.
        """
        data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": 100.00,
            "product_type": "single",
            "sales_channel_name": self.sales_channel.name,
            "stock_quantity": self.product_stock.quantity,
        }
        response = self.client.post("/api/v1/products/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, "Test Product")

    def test_get_product_list_empty(self):
        """
        Tests that the API returns a 204 No Content status when the product list is empty.
        """
        url = "/api/v1/products/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_single_product(self):
        """
        Tests fetching details of a single product.
        """
        product = Product.objects.create(
            name="Detailed Product",
            description="Detail Description",
            price=250.00,
            product_type="single",
            sales_channel=self.sales_channel,
            stock=self.product_stock,
        )
        url = f"/api/v1/products/{product.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Detailed Product")

    def test_get_product_list_non_empty(self):
        """
        Tests that the API returns a 200 OK status when the product list is not empty.
        """
        Product.objects.create(
            name="Product to List",
            description="List Description",
            price=300.00,
            product_type="single",
            sales_channel=self.sales_channel,
            stock=self.product_stock,
        )
        url = "/api/v1/products/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # Checks that there is exactly one product in the list

    def test_create_product_with_invalid_data(self):
        """
        Tests creating a product with invalid data.
        """
        url = "/api/v1/products/"
        data = {}  # Invalid data
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product(self):
        """
        Tests product update.
        """
        product = Product.objects.create(
            name="Initial Product",
            description="Initial Description",
            price=50.00,
            product_type="single",
            sales_channel=self.sales_channel,
            stock=self.product_stock,
        )
        data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 150.00,
            "sales_channel_name": self.sales_channel.name,
            "stock_quantity": 150,
        }
        response = self.client.put(
            f"/api/v1/products/{product.pk}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, "Updated Product")
        self.assertEqual(product.price, 150.00)

    def test_delete_product(self):
        """
        Tests product deletion.
        """
        product = Product.objects.create(
            name="Product to be Deleted",
            description="Description to be Deleted",
            price=200.00,
            product_type="single",
            sales_channel=self.sales_channel,
            stock=self.product_stock,
        )
        response = self.client.delete(f"/api/v1/products/{product.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
