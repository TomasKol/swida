"""Serializers for model Order"""

from rest_framework import serializers

from transport_management_core.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Basic serializer for model Order"""

    class Meta:
        model = Order
        fields = "__all__"
