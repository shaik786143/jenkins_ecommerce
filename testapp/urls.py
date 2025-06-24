from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"products", views.ProductViewSet, basename="product")
router.register(r"sales", views.SaleViewSet, basename="sale")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
    path("create-payment-intent/", views.create_payment_intent, name="create_payment_intent"),
    path("stripe-webhook/", views.stripe_webhook, name="stripe_webhook"),
    path('products/', views.ProductListView.as_view(), name='product-list'),
] 