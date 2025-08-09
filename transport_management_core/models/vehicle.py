"""Django ORM model for Vehicle"""

from dataclasses import dataclass

from django.db import models
from django.utils.functional import cached_property


@dataclass
class CurrentPosition:
    x_coordinate: int
    y_coordinate: int


class VehicleTypeChoices(models.TextChoices):
    """Possible values for Vehicle.vehicle_type"""

    TRUCK = "truck", "truck"
    VAN = "van", "van"


class Vehicle(models.Model):
    """Django ORM model for Vehicle"""

    license_plate_number = models.CharField(max_length=10, unique=True)
    vehicle_type = models.CharField(max_length=5, choices=VehicleTypeChoices.choices)
    max_capacity = models.PositiveIntegerField(
        help_text="Max capacity of the vehicle in kg"
    )
    cost_per_km = models.FloatField(help_text="Cost of transport in €/km")
    is_available = models.BooleanField()

    @cached_property
    def current_position(self):
        """Get the coordinates of the latest recorded (aka current) position"""
        position = self.position_set.order_by("-timestamp").first()
        if position:
            return CurrentPosition(
                x_coordinate=position.x_coordinate, y_coordinate=position.y_coordinate
            )
        return None

    def __str__(self):
        return f"{self.vehicle_type} {self.license_plate_number}"
