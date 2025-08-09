import factory

from transport_management_core.models import Address, Driver, Order, Position, Vehicle


class AddressFactory(factory.django.DjangoModelFactory):
    x_coordinate = -1
    y_coordinate = -1

    class Meta:
        model = Address


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
    pickup_address = factory.SubFactory(AddressFactory)
    delivery_address = factory.SubFactory(AddressFactory)
    vehicle = factory.SubFactory(VehicleFactory)
    driver = factory.SubFactory(DriverFactory)
    weight = 12.3

    class Meta:
        model = Order


class PositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Position
