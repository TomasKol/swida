"""Django ORM model for Position"""

from django.db import models


class Position(models.Model):
    """Django ORM model for Position"""

    vehicle = models.ForeignKey("Vehicle", on_delete=models.CASCADE)
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
