import requests
import json

from constants import GEOCODE_API_KEY, GEOCODE_API_URL


def get_zip_code(geocoding_res):
    zipcode = None
    status = geocoding_res['status']

    if status != 'OK':
        return zipcode

    results = geocoding_res['results'][0]
    add_components = results['address_components']

    for comps in add_components:
        types = comps['types'][0]

        if types == 'postal_code':
            zipcode = comps['long_name']
            return zipcode

    return zipcode


def get_formatted_address(geocoding_res):
    status = geocoding_res['status']
    if status == 'OK':
        results = geocoding_res['results'][0]
        address = results['formatted_address']
        return True, address
    else:
        return False, 'cannot get formatted address'


def get_lat_and_long(geocoding_res):
    lat, lng = None, None
    status = geocoding_res['status']
    if status != 'OK':
        return None, None
    try:
        results = geocoding_res['results'][0]
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
    except:
        pass
    return lat, lng


def get_geocoding_data(address_or_zipcode):
    api_key = GEOCODE_API_KEY
    endpoint = f"{GEOCODE_API_URL}?address={address_or_zipcode}&key={api_key}"
    try:
        geocoding_res = requests.get(endpoint)
        return geocoding_res.json()
    except:
        return None
