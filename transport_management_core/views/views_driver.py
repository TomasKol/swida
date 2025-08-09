from rest_framework import generics

from transport_management_core.models.driver import Driver
from transport_management_core.serializers.serializers_driver import DriverSerializer


class DriverListView(generics.ListCreateAPIView):
    """List and Create view for model Driver"""

    serializer_class = DriverSerializer
    queryset = Driver.objects.all()


class DriverDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get detail, edit and delete view for model Driver"""

    serializer_class = DriverSerializer
    queryset = Driver.objects.all()
    lookup_field = "pk"
