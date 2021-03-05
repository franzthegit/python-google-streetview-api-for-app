from get_street_view_data import extract_street_view_metadata
from get_image_url import get_default_image, get_image_url, get_satellite_image_url
from get_geocoding_data import get_geocoding_data, get_formatted_address, get_lat_and_long


def success(address):
    print("success")
    return get_image_url(address)


def not_found(address):
    geo_data = get_geocoding_data(address)
    if geo_data == None:
        return None

    address_data = get_formatted_address(geo_data)
    got_corrected_address = address_data[0]
    if got_corrected_address == True:
        print("getting corrected address")
        corrected_address = address_data[1]
        print(corrected_address)
        metadata = extract_street_view_metadata(corrected_address)
        if metadata == None:
            return None

        status = metadata['status']
        return metadata_processor(corrected_address, status)
    else:
        print("cannot get corrected address")
        return get_default_image()


def zero_results(address):
    print("fetching satellite view")
    return get_satellite_image_url(address)
    # geo_data = get_geocoding_data(address)
    # if geo_data == None:
    #     return None

    # lat_lng_value = get_lat_and_long(geo_data)
    # lat = lat_lng_value[0]
    # lng = lat_lng_value[1]

    # if lat == None or lng == None:
    #     print("lat lng error")
    #     return get_default_image()

    # metadata = extract_street_view_metadata(lat_lng_value)
    # if metadata == None:
    #     return None

    # status = metadata['status']

    # if status == 'OK':
    #     print("nearby street view image")
    #     return get_image_url(lat_lng_value)
    # else:
    #     print("cannot find nearby")
    #     return get_default_image()


def error_case(address):
    print("fetching satellite view")
    return get_satellite_image_url(address)


def metadata_processor(address, status):
    print(f"-----------------     {status}     ---------------------")
    options = {
        'OK': success,
        'NOT_FOUND': not_found,
        'ZERO_RESULTS': zero_results,
        'OVER_DAILY_LIMIT': error_case,
        'OVER_QUERY_LIMIT': error_case,
        'REQUEST_DENIED': error_case,
        'INVALID_REQUEST': error_case,
        'UNKNOWN_ERROR': error_case,
    }

    check = options[status]
    return check(address)
