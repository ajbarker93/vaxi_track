from django.core.mail import send_mail
from django.template.loader import render_to_string

from . import core
from .models import Counter

import numpy as np
from random import randint

def centre_register_html(data_dict, csrf_token=None):

        # Email shot is just the same HTML as we're serving to the browser
        if data_dict['email']:
            id = randint(100000, 999999)
            fname = data_dict['cname']
            email = data_dict['email']
            send_mail(f'Vaxitrack login for {cname} is {id}', "",
                    'vaxitrack@gmail.com', [nhs_email], fail_silently=False,
                    html_message=html)
        return html
