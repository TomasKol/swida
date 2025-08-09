"""Django ORM model for Order"""

from django.db import models


class OrderStatusChoices(models.TextChoices):
    """Possible values for Order.status"""

    NEW = "new", "new"
    ASSIGNED = "assigned", "assigned"
    IN_TRANSIT = "in transit", "in transit"
    DELIVERED = "delivered", "delivered"
    CLOSED = "closed", "closed"


class Order(models.Model):
    """Django ORM model for Order"""

    order_number = models.CharField(max_length=15, unique=True)
    vehicle = models.ForeignKey(
        "Vehicle", null=True, blank=True, on_delete=models.SET_NULL
    )
    driver = models.ForeignKey(
        "Driver", null=True, blank=True, on_delete=models.SET_NULL
    )
    customer_name = models.CharField(max_length=15)
    pickup_address = models.CharField(max_length=15)
    delivery_address = models.CharField(max_length=15)
    weight = models.FloatField(help_text="Total weight of the load in kg")
    status = models.CharField(
        choices=OrderStatusChoices.choices, default=OrderStatusChoices.NEW
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_number} - {self.status}"
