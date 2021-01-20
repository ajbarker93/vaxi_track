from django import forms
from django.template.defaultfilters import mark_safe

class RegForm(forms.Form):

    cname = forms.CharField(label='Centre name', required=True, strip=True)
    pc = forms.CharField(label='Postcode',
                required=True, strip=True)
    email =forms.CharField(label='NHS email',
                required=True, help_text="Your login code will be sent to NHS.net email")

class LogForm(forms.Form):

    id = forms.CharField(label='VaxiTrack ID', required=True, strip=True)
    doses_available = forms.CharField(label='Doses today',required=True, strip=True)
    start_time = forms.CharField(label='Time available',required=True, strip=True)
    type = forms.CharField(label='Vax type', required=True, strip=True, help_text="Use 24hr format, e.g. 1500. Vax type is Pfizer or Oxford-AZ",)

class UserForm(forms.Form):

    name = forms.CharField(label='Name',required=True, strip=True)
    email = forms.CharField(label='Email address', required=True)
    postcode = forms.CharField(label='Postcode', required=True)
    age = forms.CharField(label='Age',required=True, help_text="We'll email you if a vaccine is available")
