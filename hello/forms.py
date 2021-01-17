from django import forms

class BuildForm(forms.Form):
    fpath = forms.FileField(label='Input data', help_text="excel .xls or .xlsx")
    email = forms.EmailField(label='Email address',
                help_text="(optional) send results via email; NHS.net suggested", required=False)
