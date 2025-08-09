import factory
from transport_management_core.models import Driver, Order, Position, Vehicle


class DriverFactory(factory.django.DjangoModelFactory):
    is_available = True

    class Meta:
        model = Driver


class VehicleFactory(factory.django.DjangoModelFactory):
    is_available = True
    max_capacity = 123
    cost_per_km = 12.3

    class Meta:
        model = Vehicle


class OrderFactory(factory.django.DjangoModelFactory):
    vehicle = factory.SubFactory(VehicleFactory)
    driver = factory.SubFactory(DriverFactory)
    weight = 12.3

    class Meta:
        model = Order


class PositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Position
