from django import forms
from django.template.defaultfilters import mark_safe

import numpy as np
from random import randint

from .models import Centre, User

class LogForm(forms.ModelForm):

    class Meta:
        model = Centre
        fields = ('VaxiTrack_ID', 'available_at', 'doses_available','vax_type')

class RegForm(forms.ModelForm):

    class Meta:
        model = Centre
        fields = ('centre_name', 'postcode', 'email',)

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'postcode', 'age',)
