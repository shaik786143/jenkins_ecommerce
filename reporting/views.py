from django.shortcuts import render
from rest_framework import viewsets
from .models import DailySaleSummary
from .serializers import DailySaleSummarySerializer

# Create your views here.

class DailySaleSummaryViewSet(viewsets.ModelViewSet):
    queryset = DailySaleSummary.objects.all().order_by('-summary_date')
    serializer_class = DailySaleSummarySerializer
