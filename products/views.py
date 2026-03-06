from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, Http404
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status

class ProductListAPIView(ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "message": "Products retrieved successfully",
            "data": serializer.data
        })

class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            # Tangani 404 custom
            return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response(
                {
                    "success": False,
                    "message": "Product not found",
                    "errors": None
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(instance)
        return Response(
            {
                "success": True,
                "message": "Product retrieved successfully",
                "data": serializer.data
            }
        )