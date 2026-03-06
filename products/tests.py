from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product

# Create your tests here.
class ProductAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.product1 = Product.objects.create(
            name="Mechanical Keyboard",
            price=750000,
            description="RGB Mechanical Keyboard",
            stock=20
        )

        self.product2 = Product.objects.create(
            name="Gaming Mouse",
            price=350000,
            description="High precision gaming mouse",
            stock=40
        )

    # GET ALL PRODUCTS
    def test_get_products(self):
        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Products retrieved successfully")

    # GET PRODUCT DETAIL
    def test_get_product_detail(self):
        response = self.client.get(f"/api/products/{self.product1.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Product retrieved successfully")

        self.assertEqual(response.data["data"]["id"], self.product1.id)
        self.assertEqual(response.data["data"]["name"], self.product1.name)

    # PRODUCT DETAIL NOT FOUND
    def test_product_detail_not_found(self):

        non_existent_id = self.product2.id + 100
        response = self.client.get(f"/api/products/{non_existent_id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["message"], "Product not found")