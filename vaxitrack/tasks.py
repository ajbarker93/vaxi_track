from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Counter, User, Centre

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

def find_and_assign(centre_id, n_doses):

    # Find patient IDs within range of this centre
    centre = Centre.objects.get(id__exact=centre_id)
    pids = centre.find_closest_patients(0.1)

    # Sort by age ASCENDING, select the last N
    pats = User.objects.in_bulk(pids).values()

    if not pats:
        return

    pats = sorted(pats, key=lambda x: x.age)
    pats = pats[-n_doses:]

    success = []
    for idx,pat in enumerate(pats):

        try:
            pat.assign_dose(centre_id)
            success.append(idx)
        except Exception as e:
            msg = f"Error assigning user {pat.id} to centre {centre_id}.\n"
            msg += f"Original exception\n: {str(e)}"
            print(msg)

    emails = [pats[ss].email for ss in success]
    centre.send_pat_email(emails)

    # Increment the counter with assigned doses
    Counter.increment(centres=0, vaccines=n_doses, patients=0)
