from API_KEY import GEOCODE_API_KEY, STREET_IAMGE_KEY, MAPS_SECRET_KEY
# Test Files

SRC_FILE_NAME = '19396 - Mailing List draft v2 - for images'


ASSETS_DIR = "assets/"
DOWNLOADED_DIR = 'assets\\noziptest\\ivorydownloads\\'
GDRIVE_DIR = 'Q:\Shared drives\StreetViewImages\\'

DES_FILE_SUFFIX = " - IMAGES"
DATA_FILE_FORMAT = '.csv'

SRC_FILE_URL = f"{ASSETS_DIR}{SRC_FILE_NAME}{DATA_FILE_FORMAT}"
DES_FILE_URL = f"{ASSETS_DIR}{SRC_FILE_NAME}{DES_FILE_SUFFIX}{DATA_FILE_FORMAT}"

# Google Map Geocoding

GEOCODE_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"


# Google Map Street View

STREET_METADATA_URL = "https://maps.googleapis.com/maps/api/streetview/metadata"
STREET_IMAGE_URL = "https://maps.googleapis.com/maps/api/streetview"
MAPS_SATELLITE_URL = "https://maps.googleapis.com/maps/api/staticmap"

API_KEY = STREET_IAMGE_KEY
IMAGE_SIZE = '640x420'
FOV = 70


# Flag value for Satellite View

INCLUDE_SATELLITE_VIEW = True
INCLUDE_SATELLITE_MARKER = True


# Default Download Format


GDRIVE_DEFAULT_IMAGE = f"{GDRIVE_DIR}default.png"
DOWNLOADED_EXTENSION = '.jpg'

# Table Header

ADDRESS_INF_HEADERS = ['Image Address',
                       'Image City', 'Image State', 'Image Zip']
APPEND_HEADERS = ['Status', 'Street View URL', 'Street View Image Location']

if INCLUDE_SATELLITE_VIEW:
    APPEND_HEADERS.extend(['Satellite View URL', 'Satellite View Image Location'])

# Set Sleep Time for the visualization
SLEEP_TIME = 0.2
