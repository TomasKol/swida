"""Serializers for model Driver"""

from rest_framework import serializers

from transport_management_core.models import Address


class AddressSerializer(serializers.ModelSerializer):
    """Basic serializer for model Address"""

    class Meta:
        model = Address
        fields = "__all__"
