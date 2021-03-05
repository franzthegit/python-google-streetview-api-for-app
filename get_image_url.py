import requests
import os
from get_geocoding_data import get_geocoding_data, get_formatted_address, get_zip_code
from get_street_view_data import extract_street_view_image_url, extract_satellite_view_image_url

from constants import DOWNLOADED_DIR, DOWNLOADED_EXTENSION, GDRIVE_DEFAULT_IMAGE, GDRIVE_DIR


def get_default_image():
    print("using default image")
    return GDRIVE_DEFAULT_IMAGE, GDRIVE_DEFAULT_IMAGE


def download_image(src, desc):
    try:
        img_data = requests.get(src).content
        with open(desc, 'wb') as handler:
            handler.write(img_data)
        return True
    except:
        print("error caused while image downloading...")
        return False


def get_image_url(address):
    print("get_image_url")

    # geocode_res = get_geocoding_data(address)
    # print(geocode_res)

    # if geocode_res == None:
    #     return None

    # if geocode_res['status'] != 'OK':
    #     return get_default_image()

    # zip_code = get_zip_code(geocode_res)
    # if zip_code == None:
    #     return get_default_image()

    image_url = extract_street_view_image_url(address)
    print("Found Image URL")
    print(image_url)

    file_name = f"{address}"
    full_image_path = f"{DOWNLOADED_DIR}{file_name}{DOWNLOADED_EXTENSION}"
    gdrive_image_location = f"{GDRIVE_DIR}{file_name}{DOWNLOADED_EXTENSION}"
    # file_existing = os.path.isfile(full_image_path)

    print("file_name")
    print(file_name)

    print("full_image_path")
    print(full_image_path)

    print("gdrive_image_location")
    print(gdrive_image_location)




    print('file_existing?')
    file_existing = os.path.isfile(gdrive_image_location)
    print(file_existing)
    os.makedirs(DOWNLOADED_DIR, exist_ok=True)

    print("downloading image")
    download_res = download_image(image_url, gdrive_image_location)
    if download_res == False:
        return None

    # if file_existing == False:
    #     print("downloading image")
    #     download_res = download_image(image_url, gdrive_image_location)
    #     if download_res == False:
    #         return None
    # else:
    #     print("image exists")
    print("src: ", image_url)
    print("des: ", gdrive_image_location)
    return image_url, gdrive_image_location

def get_satellite_image_url(address):

    # geocode_res = get_geocoding_data(address)
    # print(geocode_res)

    # if geocode_res == None:
    #     return None

    # if geocode_res['status'] != 'OK':
    #     return get_default_image()

    # zip_code = get_zip_code(geocode_res)
    # if zip_code == None:
    #     return get_default_image()

    image_url = extract_satellite_view_image_url(address)

    file_name = f"{address}-satellite"
    full_image_path = f"{DOWNLOADED_DIR}{file_name}{DOWNLOADED_EXTENSION}"
    gdrive_image_location = f"{GDRIVE_DIR}{file_name}{DOWNLOADED_EXTENSION}"
    # file_existing = os.path.isfile(full_image_path)
    file_existing = os.path.isfile(gdrive_image_location)
    os.makedirs(DOWNLOADED_DIR, exist_ok=True)

    if file_existing == False:
        print("downloading satellite image")
        download_res = download_image(image_url, gdrive_image_location)
        if download_res == False:
            return None
    else:
        print("satellite image exists")
    print("src: ", image_url)
    print("des: ", gdrive_image_location)
    return image_url, gdrive_image_location