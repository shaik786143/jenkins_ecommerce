from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailySaleSummaryViewSet

router = DefaultRouter()
router.register(r'daily_summaries', DailySaleSummaryViewSet, basename='daily_summary')

urlpatterns = [
    path('', include(router.urls)),
] 