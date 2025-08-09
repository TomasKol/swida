from django.urls import path

from transport_management_core.views.views_driver import (
    DriverDetailView,
    DriverListView,
)
from transport_management_core.views.views_order import OrderDetailView, OrderListView
from transport_management_core.views.views_position import (
    PositionCreateView,
    PositionDetailView,
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
    path("/vehicles/", VehicleListView.as_view()),
    path("/vehicles/<int:pk>/", VehicleDetailView.as_view()),
    path("/vehicles/<int:vehicle_id>/positions/", PositionCreateView.as_view()),
    path("/vehicles/<int:vehicle_id>/positions/<int:pk>/", PositionDetailView.as_view()),
]
