from django.db import models
from django.core import validators
from django.core.mail import send_mail
from django.conf import settings

import numpy as np
from random import randint

from .core import geocode


class Counter(models.Model):

    centres = models.BigIntegerField(default=0)
    vaccines = models.BigIntegerField(default=0)
    patients = models.BigIntegerField(default=0)

    @classmethod
    def increment(cls, centres, vaccines,patients):
        c = cls.objects.all()
        assert len(c) == 1, 'there can only be one counter'
        c = c[0]
        c.routes += centres
        c.locations += vaccines
        c.patients += patients
        c.save()

    @classmethod
    def read(cls):
        c = cls.objects.all()
        assert len(c) == 1, 'there can only be one counter'
        c = c[0]
        return c.vaccines, c.centres, c.patients


class Centre(models.Model):

    doses_available = models.CharField(max_length=10, default='')
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    postcode = models.CharField(max_length=10)
    centre_name = models.CharField(max_length=30,default='')
    vax_type = models.CharField(max_length=30,default='')
    email = models.EmailField(null=True)
    VaxiTrack_ID = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    available_at = models.CharField(max_length=30,default='')
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, postcode, email):

        if Centre.objects.filter(postcode__exact=postcode).filter(email__exact=email):
            raise ValueError("A centre with this postcode and email already exists")

        cent = cls()
        lat_long = geocode(postcode)
        vt_int = randint(1e5,1e6-1)
        cent.VaxiTrack_ID = vt_int
        cent.email = email
        cent.latitude = lat_long[0]
        cent.longitude = lat_long[1]
        cent.postcode = postcode
        cent.save()
        return cent

    def __repr__(self):
        s = (f"Centre id: {self.id}, postcode: {self.postcode}, "
            f"lat_long: {self.location}, email: {self.email},"
            f"doses available: {self.doses_available}, VaxiTrack_ID: {self.VaxiTrack_ID}")
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

    def set_time_available(self, new_value):
        """
        Set the value of time available for vax
        """

        self.available_at = new_value
        self.save()

    def set_type(self, new_value):
        """
        Set the value of doses type
        """

        self.vax_type = new_value
        self.save()

    def log_email(self):
        msg = f"This is an email to {self.centre_name} with Centre ID {self.VaxiTrack_ID}. You have logged {self.doses_available} doses of {self.vax_type} available at {self.available_at} today."
        send_mail('Vaxitrack', msg, settings.EMAIL_HOST_USER,
                    [self.email], fail_silently=False)

    def send_email(self):
        msg = f"This is an email to a Centre. Your ID is {self.VaxiTrack_ID}"
        send_mail('Vaxitrack', msg, settings.EMAIL_HOST_USER,
                    [self.email], fail_silently=False)

    def find_closest_patients(self, max_dist=0.1):
        """
        Returns patients within max_dist from the centre

        Args:
            max_dist (float): only search for patients below this radius

        Returns:
            tuple of (np.array), patients
        """

        centre_loc = (self.latitude, self.longitude)
        pats = User.objects.all()

        # Filter patients by email
        emails = pats.email

        dists = np.zeros(len(pats), dtype=float32)
        for pat in enumerate(pats):
            pat_loc = (pat.latitude, pat.longitude)
            dists[pat] = np.linalg.norm(centre_loc - pat_loc, ord=2, axis=-1)
            in_range = (dists <= max_dist)

        return emails[in_range], dists[in_range]


class User(models.Model):
    age = models.CharField(max_length=10,default='')
    email = models.EmailField(null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    postcode = models.CharField(max_length=10)
    assigned_centre = models.CharField(max_length=10,default='')
    assigned_centre_name = models.CharField(max_length=20,default='')
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

    def assign_dose(self, centre_postcode):
        """
        Assign user to a centre, reduce the doses available at that centre.

        Args:
            centre_postcode (char): centre postcode to assign to

        Raises:
            ValueError if the centre does not have any doses available
        """

        cent = Centre.objects.filter(postcode=centre_postcode)[0]
        if cent.doses_available < 1:
            raise ValueError("Centre does not have any doses available")

        self.assigned_centre = centre_postcode
        self.assigned_centre_name = cent.centre_name
        cent.doses_available -= 1
        cent.save()
        self.save()

    def send_email(self):
        msg = f"This is an email to a User. We will let you know if a dose is available today near {self.postcode} ."
        send_mail('Vaxitrack', msg, settings.EMAIL_HOST_USER,
                    [self.email], fail_silently=False)

    def send_vax_email(self,centre_name,centre_postcode,vax_time):
        msg = f"This is an email to a User. We have found you a vaccine at {centre_name}, {centre_postcode}. Please attend at {vax_time}."
        send_mail('Vaxitrack', msg, settings.EMAIL_HOST_USER,
                    [self.email], fail_silently=False)
