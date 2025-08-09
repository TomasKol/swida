"""Django ORM model for Driver"""

from django.db import models


class Driver(models.Model):
    """Django ORM model for Driver"""

    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    license_number = models.CharField(max_length=15, unique=True)
    is_available = models.BooleanField()

    def __str__(self):
        return f"{self.name}"
