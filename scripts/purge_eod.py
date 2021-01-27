from vaxitrack.models import User, Centre, Counter
from django.core.mail import send_mail
from django.conf import settings

def run():

    """
    Remove all patients at end of day from db, send a 'sorry' email to unassigned users

    Args: None
    Raises: email to purged users to tell them they haven't been successful today

    """

    pats = User.objects.filter(assigned_centre_id__lt=1)
    pp = pats.values()
    for idx,pat in enumerate(pp):
        msg = f"Hi, this is VaxiTrack. We have been unable to find you a dose near {pat['postcode']} today. Please try again tomorrow, as centres log spare vaccines everyday. Thanks, VaxiTrack"
        send_mail('VaxiTrack', msg, settings.EMAIL_HOST_USER,[pat['email']], fail_silently=False)

    cents = Centre.objects.all()
    for idx,cent in enumerate(cents):
        cent.doses_available = 0
        cent.available_at = ''

    pats.delete()
