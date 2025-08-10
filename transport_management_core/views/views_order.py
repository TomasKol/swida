from rest_framework import generics
from rest_framework.response import Response

from transport_management_core.handlers import OptimalVehicleFinder
from transport_management_core.models import Order
from transport_management_core.serializers.serializers_order import (
    AssignOptimalVehicleSerializer,
    OrderSerializer,
)


class OrderListView(generics.ListCreateAPIView):
    """List and Create view for model Order"""

    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get detail, edit and delete view for model Order"""

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = "pk"


class AssignOptimalVehicleView(generics.GenericAPIView):
    """Assign the closest available Vehicle to specified Order"""

    queryset = Order.objects.filter(vehicle__isnull=True)
    serializer_class = AssignOptimalVehicleSerializer
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        """Assign the closest available Vehicle to specified Order"""

        order = self.get_object()
        finder = OptimalVehicleFinder(order)
        serializer = self.serializer_class(instance=finder.result)
        return Response(serializer.data, status=200)
