from django import forms

class BuildForm(forms.Form):

    email = forms.EmailField(label='Email address',
                help_text="Login code sent via email; NHS.net required", required=True)
    pc = forms.CharField(label='Postcode',
                required=True, strip=True)
