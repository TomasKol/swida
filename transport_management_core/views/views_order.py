from rest_framework import generics

from transport_management_core.models import Order
from transport_management_core.serializers.serializers_order import OrderSerializer


class OrderListView(generics.ListCreateAPIView):
    """List and Create view for model Order"""

    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get detail, edit and delete view for model Order"""

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = "pk"
