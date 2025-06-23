from rest_framework import serializers
from .models import DailySaleSummary

class DailySaleSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySaleSummary
        fields = '__all__' 