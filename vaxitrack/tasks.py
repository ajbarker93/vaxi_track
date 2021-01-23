from django.core.mail import send_mail
from django.template.loader import render_to_string

from . import core
from models import Counter, User, Centre


# When a vax centre logs N vaccines, do the following:

# 1. Find separation between centre and all users in the db. One degree of latitude/longitude is 111km, so:
# separation = 111*np.sqrt( (User.latitude - Centre.latitude)**2 + (User.latitude - Centre.latitude)**2)
# (in km)

# 2. Select from users where separation < 10
# 3. Descending sort the remaining users
# 4. Choose top N users
# 5. For each user in the top N, send a success email with centre info (name, postcode, time available)
# 6. Remove N vaccines from centre
# 6. Remove top N users from queue
# 7. Increment counter etc.


def find_and_assign(data_dict):

    # Find number and info on centre from which to assign
    num_to_assign = data_dict['doses_available']
    centre_id = data_dict['VaxiTrack_ID']
    postcode = data_dict['postcode']
    vax_time = data_dict['available_at']
    centre_name = data_dict['centre_name']

    # Find emails of patients within range
    emails = Centre.find_closest_patients(data_dict)

    # Find users with those emails
    pats = User.objects.filter(email__exact=emails)

    # Descending sort the patients by age
    pats_ordered = pats.order_by('-age')

    # Choose the top N, depending on the number of doses
    pats_selected = pats_ordered[:num_to_assign]

    # Inform the selected patients they've been assigned to a centres
    # Update assigned centre for pats_selected
    pats_selected.assign_dose(postcode)

    # Send email to those with assigned centres
    pats_selected.send_vax_email(centre_name,postcode,vax_time)

    # Increment the counter with assigned doses
    #Counter.increment(len(routes), df.shape[0])
