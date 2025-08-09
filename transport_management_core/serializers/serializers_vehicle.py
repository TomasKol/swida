"""Serializers for model Vehicle"""

from rest_framework import serializers

from transport_management_core.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    """Basic serializer for model Vehicle"""

    class Meta:
        model = Vehicle
        fields = "__all__"
