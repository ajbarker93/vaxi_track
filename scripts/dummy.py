from vaxitrack.models import User, Centre

def run():

    User.objects.all().delete()
    Centre.objects.all().delete()
    Counter.objects.all().delete()

    c = Centre.create("Stable","OX13BH", "ajbarker93@gmail.com")
    c.doses_available = 2
    c.available_at = '16:00'
    c.save()

    c = Centre.create("Magdalen","OX14AU", "vaximap@gmail.com")
    c.doses_available = 3
    c.available_at = '15:00'
    c.save()

    User.create("OX37DQ", "heather.c_94@hotmail.co.uk", 27)
    User.create("OX39DU", "vaximap@gmail.com", 26)
    User.create("OX20HH", "ajbarker93@gmail.com", 29)

    c = Counter()
    c.save()
