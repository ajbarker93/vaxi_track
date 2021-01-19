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

    User.create("OX37DQ", "Adam.Barker@Squarepoint-Capital.com", 25)
    User.create("OX39DU", "vaximap@gmail.com", 26)
    User.create("OX20HH", "tomfrankkirk@gmail.com", 27)


    # accessing specific objects, examples below. 
    # get retries a single object, whereas a filter call collects a list
    # you can use any attribute defined on the object, eg doses_available, 
    # and then append __gt to turn into 'greater than' bool operation 
    # read this; https://docs.djangoproject.com/en/3.1/topics/db/queries/#retrieving-objects
    u1 = User.objects.get(email="Adam.Barker@Squarepoint-Capital.com")
    cents = Centre.objects.filter(doses_available__gt=0)