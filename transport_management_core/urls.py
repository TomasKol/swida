from django.urls import path

from transport_management_core.views.views_driver import (
    DriverDetailView,
    DriverListView,
)
from transport_management_core.views.views_order import (
    AssignOptimalVehicleView,
    OrderDetailView,
    OrderListView,
)
from transport_management_core.views.views_position import (
    PositionCreateView,
)
from transport_management_core.views.views_vehicle import (
    VehicleDetailView,
    VehicleListView,
)

urlpatterns = [
    path("/drivers/", DriverListView.as_view()),
    path("/drivers/<int:pk>/", DriverDetailView.as_view()),
    path("/orders/", OrderListView.as_view()),
    path("/orders/<int:pk>/", OrderDetailView.as_view()),
    path(
        "/orders/<int:pk>/assign-optimal-vehicle/", AssignOptimalVehicleView.as_view()
    ),
    path("/vehicles/", VehicleListView.as_view()),
    path("/vehicles/<int:pk>/", VehicleDetailView.as_view()),
    path("/positions/", PositionCreateView.as_view()),
]
