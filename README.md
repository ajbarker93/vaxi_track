# VaxiTrack: no vaccine should go to waste

This is a very simple app that has been built quickly. If you think it could be improved, please feel free to make changes to the code.

## Overview

The ambition of this app is to allow vaccine centres to quickly log spare vaccine doses, which may arise due to missed appointments, miscalculations or from spare built into the normal vaccine programme for that day. Vaccine centres can quickly log how many vaccines, which vaccine type, and what time they will be available. Users can check where the nearest vaccines are (limited to a 10 mile radius) and register to receive these.

All clinical logging is out of our hands, and we take no responsibility for delivery, follow-ups or information about the vaccine - we simply help clinicians use their spare vaccines.

With fewer vaccines wasted, we can see this pandemic off quicker!

## Site structure

This is a django website that logs spare vaccine information provided by vaccine centres and shows users where the nearest spares are to their location. The site is currently hosted on Heroku.


## License and copyright
Licensing is TBD, but the site may freely be used at XXX.
Copyright is asserted over all code contained within this repo (AJ Barker, RMT Staruch, TF Kirk, 2021).


## Set up the DB with a dummy user and centre
first
```
$ python manage.py migrate
$ python manage.py shell
```
then:
```python
from vaxitrack.models import User, Centre
c = Centre()
c.postcode = "OX13BH"
c.doses_available = 5
c.email = "ajbarker93@gmail.com"
c.save()

u = User()
u.postcode = "OX14AU"
u.email = "ajbarker93@gmail.com"
u.save()
```

then exit the shell, and run the server as usual.
