from rest_framework import generics

from transport_management_core.models.vehicle import Vehicle
from transport_management_core.serializers.serializers_vehicle import VehicleSerializer


class VehicleListView(generics.ListCreateAPIView):
    """List and Create view for model Vehicle"""

    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()


class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get detail, edit and delete view for model Vehicle"""

    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    lookup_field = "pk"
