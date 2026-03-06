import requests, base64
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from products.models import Product
from django.conf import settings

MIDTRANS_API = "https://app.sandbox.midtrans.com/snap/v1/transactions"
SERVER_KEY = settings.MIDTRANS_SERVER_KEY

class CreateOrderAPIView(APIView):

    @transaction.atomic
    def post(self, request):
        items_data = request.data.get("items", [])
        if not items_data:
            return Response({"success": False, "message": "Items required"}, status=status.HTTP_400_BAD_REQUEST)

        total = 0
        order_items = []

        for item in items_data:
            try:
                product = Product.objects.select_for_update().get(pk=item["product_id"])
            except Product.DoesNotExist:
                return Response({"success": False, "message": f"Product id {item['product_id']} not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check stock
            qty = item.get("quantity", 0)
            if product.stock < qty:
                return Response({"success": False, "message": f"Not enough stock for {product.name}"}, status=status.HTTP_400_BAD_REQUEST)

            #Reduce stock
            product.stock -= qty
            product.save()

            order_items.append({"product": product, "quantity": qty, "price": product.price})
            # Total price
            total += product.price * qty

        order = Order.objects.create(total=total)

        for oi in order_items:
            OrderItem.objects.create(order=order, product=oi["product"], quantity=oi["quantity"], price=oi["price"])

        # Create Midtrans Snap transaction
        payload = {
            "transaction_details": {"order_id": f"{order.id}", "gross_amount": total},
            "credit_card": {"secure": True},
            "customer_details": {"first_name": "Tesla", "email": "tesla@example.com"}
        }

        auth = base64.b64encode(f"{SERVER_KEY}:".encode()).decode()
        response_midtrans = requests.post(MIDTRANS_API, json=payload, headers={"Authorization": f"Basic {auth}"})
        snap_data = response_midtrans.json()
        order.midtrans_order_id = snap_data.get("order_id")
        order.save()

        return Response({
            "success": True,
            "message": "Order created",
            "data": {
                "order_id": order.id,
                "total": total,
                "snap_token": snap_data.get("token"),
                "redirect_url": snap_data.get("redirect_url")
            }
        }, status=status.HTTP_201_CREATED)
    
    