from django.db import models
from django.core import validators
from django.core.mail import send_mail
from django.conf import settings

import numpy as np 

from .core import geocode

class Centre(models.Model):
    doses_available = models.IntegerField(
                        validators=[validators.MinValueValidator(0)], default=0)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    postcode = models.CharField(max_length=10)
    email = models.EmailField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, postcode, email):

        if Centre.objects.filter(postcode__exact=postcode).filter(email__exact=email):
            raise ValueError("A centre with this postcode and email already exists")
        
        cent = cls()
        lat_long = geocode(postcode)
        cent.latitude = lat_long[0]
        cent.longitude = lat_long[1]
        cent.postcode = postcode
        cent.save()
        return cent 

    def __repr__(self):
        s = (f"Centre id: {self.id}, postcode: {self.postcode}, "
            f"lat_long: {self.location}, doses available: {self.doses_available}")
        return s 

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

    def send_email(self):
        msg = f"This is an email to a Centre. Your ID is {self.id}"
        send_mail('Vaxitrack', msg, settings.EMAIL_HOST_USER,
                    [self.email], fail_silently=False)


class User(models.Model):
    age = models.IntegerField(
                        validators=[validators.MinValueValidator(0)], default=0)
    email = models.EmailField(null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0) 
    postcode = models.CharField(max_length=10)
    assigned_centre = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, postcode, email, age):

        if User.objects.filter(email__exact=email): 
            raise ValueError("A user with that email already exists")

        u = User()
        u.email = email 
        lat_long = geocode(postcode)
        u.latitude = lat_long[0]
        u.longitude = lat_long[1]
        u.postcode = postcode 
        u.age = age 
        u.save() 
        return u

    def __repr__(self):
        s = (f"User id: {self.id}, age: {self.age}, postcode: {self.postcode}, "
            f"lat_long: {self.location}, assigned_centre: {self.assigned_centre}")
        return s 

    @property
    def location(self):
        """Latitude/longitude coordinates as array"""
        return np.array((self.latitude, self.longitude))

    def assign_dose(self, centre_id):
        """
        Assign user to a centre, reduce the doses available at that centre.
        
        Args:
            id (int): centre to assign to 
            
        Raises: 
            ValueError if the centre does not have any doses available
        """

        cent = Centre.objects.filter(id=centre_id)[0]
        if cent.doses_available < 1: 
            raise ValueError("Centre does not have any doses available")

        self.assigned_centre = centre_id
        cent.doses_available -= 1
        cent.save()
        self.save()

    def find_closest_centres(self, max_dist=0.1):
        """
        Returns IDs and distances in ascending order for the closest 
        centre within the radius max_dist from this user

        Args: 
            max_dist (float): only search centres below this radius

        Returns: 
            tuple of (np.array), centre IDs and distances, ascending
        """

        cents = Centre.objects.filter(doses_available__gt=0)
        ids = np.zeros(len(cents), dtype=int)
        locations = np.zeros((len(cents), 2), dtype=np.float32)
        for idx, cent in enumerate(cents): 
            ids[idx] = cent.id
            locations[idx,:] = (cent.latitude, cent.longitude)

        dists = np.linalg.norm(self.location - locations, ord=2, axis=-1)
        in_range = (dists <= max_dist)
        in_range_sorted = in_range[np.argsort(dists[in_range])]
        return ids[in_range_sorted], dists[in_range_sorted]

    def send_email(self):
        msg = f"This is an email to a User. Your ID is {self.id}"
        send_mail('Vaxitrack', msg, settings.EMAIL_HOST_USER,
                    [self.email], fail_silently=False)
