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
    def increment(cls, centres, vaccines, patients):
        c = cls.objects.all()
        assert len(c) == 1, 'there can only be one counter'
        c = c[0]
        c.centres += centres
        c.vaccines += vaccines
        c.patients += patients
        c.save()

    @classmethod
    def read(cls):
        c = cls.objects.all()
        assert len(c) == 1, 'there can only be one counter'
        c = c[0]
        return c.centres, c.vaccines, c.patients


class Centre(models.Model):

    doses_available = models.IntegerField(validators=[validators.MinValueValidator(0)], default=0)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    postcode = models.CharField(max_length=10)
    name = models.CharField(max_length=30,default='')
    # Set 0 to be oxford and 1 to be pfizer
    vax_type = models.IntegerField(default=0,choices=(('0','Oxford-AZ'),('1','Pfizer')))
    email = models.EmailField(null=True)
    vaxitrack_ID = models.IntegerField(default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    available_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, postcode, email):

        if Centre.objects.filter(postcode__exact=postcode).filter(email__exact=email):
            raise ValueError("A centre with this postcode and email already exists")

        cent = cls()
        lat_long = geocode(postcode)
        cent.email = email
        cent.latitude = lat_long[0]
        cent.longitude = lat_long[1]
        cent.postcode = postcode
        cent.save()
        cent.VaxiTrack_ID = "%06d" % int(cent.id)
        cent.save()
        return cent

    def __repr__(self):
        s = (f"Centre id: {self.id}, postcode: {self.postcode}, "
            f"lat_long: {self.location}, email: {self.email},"
            f"doses available: {self.doses_available}, vaxitrack_ID: {self.vaxitrack_ID}")
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
        msg = f"This is an email to {self.name} with Centre ID {self.vaxitrack_ID}. You have logged {self.doses_available} doses of {self.vax_type} available at {self.available_at} today."
        send_mail('Vaxitrack', msg, settings.EMAIL_HOST_USER,
                    [self.email], fail_silently=False)

    def send_email(self):
        msg = f"This is an email to a Centre. Your ID is {self.vaxitrack_ID}"
        send_mail('Vaxitrack', msg, settings.EMAIL_HOST_USER,
                    [self.email], fail_silently=False)

    def find_closest_patients(self, max_dist=0.1):
        """
        Returns patients within max_dist from the centre

        Args:
            max_dist (float): only search for patients below this radius

        Returns:
            list of patient ids, sorted ascending
        """

        centre_loc = self.location
        pats = User.objects.all()

        plocs = np.zeros((len(pats), 2), dtype=np.float32)
        pids = np.zeros(len(pats), dtype=int)
        for idx,pat in enumerate(pats):
            plocs[idx,:] = pat.location
            pids[idx] = (pat.id)

        dists = np.linalg.norm(centre_loc - plocs, ord=2, axis=-1)
        in_range = (dists <= max_dist)

        return pids[in_range].tolist()


class User(models.Model):

    age = models.IntegerField(validators=[validators.MinValueValidator(0)], default=0)
    email = models.EmailField(null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    postcode = models.CharField(max_length=10)
    assigned_centre_id = models.IntegerField(default=0, null=True)
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
        if self.assigned_centre_id: 
            cname = Centre.objects.get(self.assigned_centre_id).name
        else: 
            cname = "None"
        s = (f"User id: {self.id}, age: {self.age}, postcode: {self.postcode}, "
            f"lat_long: {self.location}, assigned_centre: {cname}")
        return s

    @property
    def location(self):
        """Latitude/longitude coordinates as array"""
        return np.array((self.latitude, self.longitude))

    def assign_dose(self, centre_id):
        """
        Assign user to a centre, reduce the doses available at that centre.

        Args:
            centre_postcode (char): centre postcode to assign to

        Raises:
            ValueError if the centre does not have any doses available
        """

        cent = Centre.objects.filter(id=centre_id).get()
        if cent.doses_available < 1:
            raise ValueError("Centre does not have any doses available")

        self.assigned_centre_id = cent.id
        cent.doses_available -= 1
        cent.save()
        self.save()

    def send_email(self):
        msg = f"This is an email to a User. We will let you know if a dose is available today near {self.postcode} ."
        send_mail('Vaxitrack', msg, settings.EMAIL_HOST_USER,
                    [self.email], fail_silently=False)

    def send_vax_email(self,centre_id):

        cent = Centre.objects.filter(id__exact=centre_id).get()

        msg = f"This is an email to a User. We have found you a vaccine at {cent.name}, {cent.postcode}. Please attend at {cent.available_at}."
        send_mail('Vaxitrack', msg, settings.EMAIL_HOST_USER,
                    [self.email], fail_silently=False)
