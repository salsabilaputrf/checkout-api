from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):

    help = "Seed initial product data"

    def handle(self, *args, **kwargs):

        products = [
            {
                "name": "Mechanical Keyboard",
                "price": 750000,
                "description": "RGB mechanical keyboard with blue switches.",
                "stock": 20
            },
            {
                "name": "Gaming Mouse",
                "price": 350000,
                "description": "High precision gaming mouse with adjustable DPI.",
                "stock": 40
            },
            {
                "name": "27 Inch Monitor",
                "price": 3200000,
                "description": "27 inch IPS monitor suitable for gaming and design.",
                "stock": 10
            },
            {
                "name": "USB-C Hub",
                "price": 150000,
                "description": "Multiport USB-C hub with HDMI and USB 3.0.",
                "stock": 50
            },
            {
                "name": "Laptop Stand",
                "price": 120000,
                "description": "Aluminum laptop stand for better ergonomics.",
                "stock": 35
            },
            {
                "name": "Wireless Keyboard",
                "price": 280000,
                "description": "Slim wireless keyboard with long battery life.",
                "stock": 25
            },
            {
                "name": "Noise Cancelling Headphones",
                "price": 950000,
                "description": "Over-ear headphones with active noise cancellation.",
                "stock": 15
            },
            {
                "name": "Webcam HD 1080p",
                "price": 420000,
                "description": "Full HD webcam ideal for video meetings and streaming.",
                "stock": 30
            },
            {
                "name": "External SSD 1TB",
                "price": 1500000,
                "description": "Portable 1TB SSD with fast data transfer.",
                "stock": 12
            },
            {
                "name": "Bluetooth Speaker",
                "price": 300000,
                "description": "Portable Bluetooth speaker with deep bass.",
                "stock": 45
            }
        ]

        for p in products:
            Product.objects.update_or_create(
                name=p["name"],
                defaults={
                    "price": p["price"],
                    "description": p["description"],
                    "stock": p["stock"]
                }
            )

        self.stdout.write(
            self.style.SUCCESS("10 products seeded successfully")
        )