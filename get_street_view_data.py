import requests
import json
import urllib.parse

from constants import STREET_IAMGE_KEY, MAPS_SECRET_KEY, STREET_METADATA_URL, STREET_IMAGE_URL, MAPS_SATELLITE_URL, IMAGE_SIZE, FOV, INCLUDE_SATELLITE_MARKER
from get_geocoding_data import get_lat_and_long, get_geocoding_data
from signed_url_generator import sign_url

API_KEY = STREET_IAMGE_KEY


def extract_street_view_metadata(address_or_latlng):
    location = address_or_latlng
    endpoint = f"{STREET_METADATA_URL}?size={IMAGE_SIZE}&fov={FOV}&location={location}&key={API_KEY}"
    res = requests.get(endpoint)
    return res.json()
    # try:
    #     res = requests.get(endpoint)
    #     return res.json()
    # except:
    #     return None

def extract_street_view_image_url(address_or_latlng):
    location = urllib.parse.quote(address_or_latlng)
    endpoint = f"{STREET_IMAGE_URL}?size={IMAGE_SIZE}&fov={FOV}&location={location}&key={API_KEY}"
    print(endpoint)
    try:
      signed_url = sign_url(endpoint, MAPS_SECRET_KEY)
      return signed_url
    except:
      return unsigned_url

def extract_satellite_view_image_url(address_or_latlng):
    geocoding_res = get_geocoding_data(address_or_latlng)
    center = get_lat_and_long(geocoding_res)
    center_lat_lng = f"{center[0]},{center[1]}"
    unsigned_url = f"{MAPS_SATELLITE_URL}?size={IMAGE_SIZE}&center={center_lat_lng}&zoom={20}&maptype=hybrid&key={API_KEY}"

    if INCLUDE_SATELLITE_MARKER:
      unsigned_url = unsigned_url + f"&markers={center_lat_lng}"

    try:
      signed_url = sign_url(unsigned_url, MAPS_SECRET_KEY)
      return signed_url
    except:
      return unsigned_url
