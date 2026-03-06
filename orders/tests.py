from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Product
from orders.models import Order, OrderItem

class OrderAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.product1 = Product.objects.create(
            name="Mechanical Keyboard",
            price=750000,
            description="RGB keyboard",
            stock=10
        )

        self.product2 = Product.objects.create(
            name="Gaming Mouse",
            price=350000,
            description="Gaming mouse",
            stock=20
        )

        self.url = "/api/orders/"

    # SUCCESS CREATE ORDER SINGLE ITEM
    def test_create_order_success(self):
        data = {
            "items": [
                {"product_id": self.product1.id, "quantity": 2}
            ]
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Order created")

        order_data = response.data["data"]
        self.assertIn("order_id", order_data)
        self.assertIn("total", order_data)
        self.assertIn("snap_token", order_data)        
        self.assertIn("redirect_url", order_data)     


    # SUCCESS CREATE ORDER MULTIPLE ITEMS
    def test_create_order_multiple_items(self):
        data = {
            "items": [
                {"product_id": self.product1.id, "quantity": 1},
                {"product_id": self.product2.id, "quantity": 3}
            ]
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Order created")

        order_data = response.data["data"]
        self.assertIn("order_id", order_data)
        self.assertIn("total", order_data)
        self.assertIn("snap_token", order_data)
        self.assertIn("redirect_url", order_data)


    # FAIL ORDER STOCK TIDAK CUKUP
    def test_order_fail_stock_not_enough(self):
        data = {"items": [{"product_id": self.product1.id, "quantity": 50}]}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["message"], f"Not enough stock for {self.product1.name}")

    # FAIL ORDER PRODUCT TIDAK DITEMUKAN
    def test_order_fail_product_not_found(self):
        data = {"items": [{"product_id": 9999, "quantity": 1}]}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["message"], "Product id 9999 not found")
