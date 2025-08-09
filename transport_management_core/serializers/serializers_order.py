"""Serializers for model Order"""

from rest_framework import serializers

from transport_management_core.models import Order
from transport_management_core.serializers.serializers_vehicle import VehicleSerializer
from transport_management_core.serializers.serializers_driver import DriverSerializer


class OrderSerializer(serializers.ModelSerializer):
    """Basic serializer for model Order"""

    driver = DriverSerializer(required=False)
    vehicle = VehicleSerializer(required=False)

    class Meta:
        model = Order
        fields = "__all__"
