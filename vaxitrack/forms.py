from django import forms
from django.template.defaultfilters import mark_safe

class BuildForm(forms.Form):

    email = forms.EmailField(label='Email address',
                help_text="Login code will be sent to NHS.net email", required=True)
    pc = forms.CharField(label='Postcode',
                required=True, strip=True)
    name=forms.CharField(label='Centre name',
                required=True, strip=True)

class LogForm(forms.Form):

    id = forms.CharField(label='Centre ID', required=True, strip=True)
    doses_available = forms.CharField(label='Doses today',required=True, strip=True)
    start_time = forms.CharField(label='Time available',required=True, strip=True)
    type = forms.CharField(label='Vax type', required=True, strip=True)
