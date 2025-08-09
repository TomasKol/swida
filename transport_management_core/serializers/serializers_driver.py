"""Serializers for model Driver"""

from rest_framework import serializers

from transport_management_core.models import Driver


class DriverSerializer(serializers.ModelSerializer):
    """Basic serializer for model Driver"""

    class Meta:
        model = Driver
        fields = "__all__"
