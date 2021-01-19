from vaxitrack.models import User, Centre
from pdb import set_trace

def run():

    User.objects.all().delete()
    Centre.objects.all().delete()

    c = Centre.create("OX13BH", "Adam.Barker@Squarepoint-Capital.com")
    c.doses_available = 2 
    c.save()

    c = Centre.create("OX14AU", "vaximap@gmail.com")
    c.doses_available = 3 
    c.save()

    User.create("OX37DQ", "Adam.Barker@Squarepoint-Capital.com")
    User.create("OX39DU", "vaximap@gmail.com")
    User.create("OX20HH", "tomfrankkirk@gmail.com")