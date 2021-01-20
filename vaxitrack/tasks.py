from django.core.mail import send_mail
from django.template.loader import render_to_string

from . import core
from .models import Counter

import numpy as np
from random import randint

def send_reg_mail(data_dict):

        id = randint(100000, 999999)
        cname = data_dict['cname']
        cpcode = data_dict['pc']
        email = data_dict['email']
        send_mail(f'Vaxitrack login for {cname} at {cpcode} is {id}', "",
                    'vaxitrack@gmail.com', [nhs_email], fail_silently=False,
                    html_message=html)
        return html
