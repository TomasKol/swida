"""Serializers for model Order"""

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from transport_management_core.models import Address, Order
from transport_management_core.serializers.serializers_address import AddressSerializer
from transport_management_core.serializers.serializers_driver import DriverSerializer
from transport_management_core.serializers.serializers_vehicle import VehicleSerializer


class OrderSerializer(serializers.ModelSerializer):
    """Basic serializer for model Order"""

    driver = DriverSerializer(required=False)
    vehicle = VehicleSerializer(required=False)
    pickup_address = AddressSerializer()
    delivery_address = AddressSerializer()

    def create(self, validated_data):
        """customized to also create the Addresses before creating the Order itself"""

        # get the data and create addresses
        pickup_address_data = validated_data.pop("pickup_address")
        delivery_address_data = validated_data.pop("delivery_address")
        pickup_address, _ = Address.objects.get_or_create(**pickup_address_data)
        delivery_address, _ = Address.objects.get_or_create(**delivery_address_data)

        # create order
        order = Order.objects.create(
            pickup_address=pickup_address,
            delivery_address=delivery_address,
            **validated_data,
        )

        return order

    def validate(self, attrs):
        """Check the addresses are not the same"""
        pickup_address = attrs.get("pickup_address")
        delivery_address = attrs.get("delivery_address")
        if (
            pickup_address is not None 
            and delivery_address is not None 
            and pickup_address["x_coordinate"] == delivery_address["x_coordinate"] 
            and pickup_address["y_coordinate"] == delivery_address["y_coordinate"]
        ):            
            raise ValidationError(detail="pickup and delivery address mut not have the same coordinates")
        
        
        return attrs


    class Meta:
        model = Order
        fields = "__all__"


class AssignOptimalVehicleSerializer(serializers.Serializer):
    """Serializer for the AssignOptimalVehicle view"""

    data = serializers.CharField()
