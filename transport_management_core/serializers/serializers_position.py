"""Serializers for model Position"""

from rest_framework import serializers

from transport_management_core.models import Position


class PositionSerializer(serializers.ModelSerializer):
    """Basic serializer for model Position"""

    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Position
        fields = "__all__"
