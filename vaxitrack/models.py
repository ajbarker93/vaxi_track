from django.db import models
from django.core import validators

import numpy as np

class Centre(models.Model):
    doses_available = models.IntegerField(
                        validators=[validators.MinValueValidator(0)])
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    postcode = models.CharField(max_length=10)

    @property
    def location(self):
        """Latitude/longitude coordinates as array"""
        return np.array((self.latitude, self.longitude))

    def set_doses(self, new_value):
        """
        Set the value of doses available
        Not to be used for matching users to centres
        """

        self.doses_available = new_value
        self.save()


class User(models.Model):
    email = models.EmailField()
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    postcode = models.CharField(max_length=10)
    assigned_centre = models.IntegerField(null=True)

    @property
    def location(self):
        """Latitude/longitude coordinates as array"""
        return np.array((self.latitude, self.longitude))

    def assign_dose(self, centre_id):
        """Assign user to a centre, reduce the doses available at that centre"""

        cent = Centre.objects.filter(id=centre_id)[0]
        if cent.doses_available < 1:
            raise ValueError("Centre does not have any doses available")

        self.assigned_centre = centre_id
        cent.doses_available -= 1
        cent.save()
        self.save()
