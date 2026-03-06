from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import hashlib

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class MidtransWebhookAPIView(APIView):
    """
    Webhook endpoint Midtrans (Sandbox)
    - Validasi signature key
    - Proteksi duplicate webhook
    - Update status order menjadi 'paid' jika capture
    """

    def post(self, request, *args, **kwargs):
        # Get data
        order_id = request.data.get("order_id")
        status_code = request.data.get("status_code")
        gross_amount = request.data.get("gross_amount")
        signature_key = request.data.get("signature_key")
        print("hit1")
        # Validation signature key
        payload = order_id + status_code + gross_amount + settings.MIDTRANS_SERVER_KEY
        generated_signature = hashlib.sha512(payload.encode()).hexdigest()

        if signature_key != generated_signature:
            return Response(
                {"success": False, "message": "Invalid signature"},
                status=status.HTTP_400_BAD_REQUEST
            )
        print("hit2")
        # Get order
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response(
                {"success": False, "message": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # ProtProtection duplicate webhook
        if order.status == "paid":
            return Response(
                {"success": True, "message": "Webhook already processed"},
                status=status.HTTP_200_OK
            )

        # Update status order based on notification webhook
        transaction_status = request.data.get("transaction_status")
        print(transaction_status)
        if transaction_status == "capture":
            order.status = "paid"
            order.midtrans_order_id = request.data.get("transaction_id")
            order.paid_at = timezone.now()
        elif transaction_status == "settlement":
            order.status = "paid"
            order.midtrans_order_id = request.data.get("transaction_id")
            order.paid_at = timezone.now()
        elif transaction_status == "pending":
            order.status = "pending"
        elif transaction_status in ["deny", "cancel", "expire"]:
            order.status = "failed"

        order.save()
        
        return Response(
            {"success": True, "message": "Order updated"},
            status=status.HTTP_200_OK
        )