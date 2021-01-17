from django.core.mail import send_mail
from django.template.loader import render_to_string

from . import core
from .models import Counter

def route_resonse_html(data_dict, csrf_token=None):

    try:
        idcol = data_dict.get('idcol', 'A')

        # Email shot is just the same HTML as we're serving to the browser
        if data_dict['email']:
            fname = data_dict['fname']
            email = data_dict['email']
            send_mail(f'Vaxitrack login for {fname}', "",
                    'vaxitrack@gmail.com', [email], fail_silently=False,
                    html_message=html)

        return html
