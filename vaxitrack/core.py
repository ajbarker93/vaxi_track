from django.conf import settings

import requests
import base64
from pdb import set_trace
import io

import pandas as pd
import numpy as np
import googlemaps


def geocode(location):
    """
    Geocode a single location via maps API
    Returns a tuple of latitude and longitude
    """
    gmaps = googlemaps.Client(key=settings.GAPI_KEY)
    loc = gmaps.geocode(location, region="UK")
    if not loc: 
        raise RuntimeError(f"Could not find {location} on Google maps")
    else:
        return (loc[0]["geometry"]["location"]["lat"], 
                loc[0]["geometry"]["location"]["lng"])