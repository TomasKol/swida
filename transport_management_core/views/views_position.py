from rest_framework import generics

from transport_management_core.models.position import Position
from transport_management_core.serializers.serializers_position import PositionSerializer


class PositionCreateView(generics.CreateAPIView):
    """Create view for model Position"""

    serializer_class = PositionSerializer
    queryset = Position.objects.all()


class PositionDetailView(generics.RetrieveAPIView):
    """Get detail view for model Position"""

    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    lookup_field = "pk"
