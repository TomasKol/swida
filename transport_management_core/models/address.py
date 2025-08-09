"""Django ORM model for Address"""

from django.db import models


class Address(models.Model):
    """Django ORM model for Address"""

    address = models.CharField(max_length=100, default="")
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()
