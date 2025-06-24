from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Product, Sale
from .serializers import ProductSerializer, SaleSerializer
from django.core.cache import cache
from rest_framework.response import Response

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        cache_key = "product_list"
        cached_data = cache.get(cache_key)

        if cached_data:
            print("[DEBUG] Cache HIT for product_list")
            return Response(cached_data)
        
        print("[DEBUG] Cache MISS for product_list")
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        # Store in cache for 5 minutes (300 seconds)
        cache.set(cache_key, data, timeout=300)
        
        return Response(data)

class SaleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sales to be viewed or edited.
    """
    queryset = Sale.objects.all().order_by("-sale_date")
    serializer_class = SaleSerializer

@csrf_exempt
def create_payment_intent(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=data["amount"],
                currency="usd",
                automatic_payment_methods={
                    "enabled": True,
                },
            )
            return JsonResponse({
                "clientSecret": intent.client_secret
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=403)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({"error": str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({"error": str(e)}, status=400)

    # Handle the event
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        # Here you would look up the product and create the sale
        # For this demo, we can't know which product was sold,
        # so we'll just log it. A real application would pass a
        # product ID in the payment metadata.
        print(f"Payment for {payment_intent['amount']} succeeded!")
        # Example: 
        # product = Product.objects.get(id=payment_intent.metadata.product_id)
        # Sale.objects.create(...)
        
    return JsonResponse({"status": "success"})

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
