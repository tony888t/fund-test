from rest_framework import serializers
from .models import Fund


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = "__all__"
