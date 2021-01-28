# VaxiTrack: no vaccine should go to waste

This is a very simple app that has been built quickly. If you think it could be improved, please feel free to make changes to the code.

## Overview

The ambition of this app is to allow vaccine centres to quickly log spare vaccine doses, which may arise due to missed appointments, miscalculations or from spare built into the normal vaccine programme for that day. Vaccine centres can quickly log how many vaccines, which vaccine type, and what time they will be available. Users can check where the nearest vaccines are (limited to a 10 mile radius) and register to receive these.

All clinical logging is out of our hands, and we take no responsibility for delivery, follow-ups or information about the vaccine - we simply help clinicians use their spare vaccines.

With fewer vaccines wasted, we can see this pandemic off quicker!

## Site structure

This is a django website that logs spare vaccine information provided by vaccine centres and shows users where the nearest spares are to their location. The site is currently hosted on Heroku.

## Data and GDPR

For the purposes of calculating proximity to a vaccination centre, we require your postcode. As we need to let you know if a vaccine is available, we require your email. Providing your age allows us to prioritise the oldest patients. All data provided by patients and vaccine centres is used for these purposes only. All users and centres who sign up to VaxiTrack agree to their data being used on these terms. We delete all records periodically thus no data is stored long term. 

## License and copyright
Licensing is TBD, but the site may freely be used at https://vaxi-track.herokuapp.com/.
Copyright is asserted over all code contained within this repo (AJ Barker, RMT Staruch, TF Kirk, 2021).
