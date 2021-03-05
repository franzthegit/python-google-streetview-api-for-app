import csv
import time
from get_street_view_data import extract_street_view_metadata
from get_image_url import get_satellite_image_url
from metadata_processor import metadata_processor
from constants import SRC_FILE_URL, DES_FILE_URL, SLEEP_TIME, INCLUDE_SATELLITE_VIEW
from spreadsheet_processor import append_headings, get_street_head_positions, check_blank_row, get_full_address_from_heading_pos, error_row


src_file = open(SRC_FILE_URL, newline='')
des_file = open(DES_FILE_URL, 'w', newline='')

csv_reader_object = csv.reader(src_file)
csv_writer_object = csv.writer(des_file)

print(f"\nReading data from {SRC_FILE_URL}...\n")
time.sleep(SLEEP_TIME)

# get head itemšs
header = next(csv_reader_object)

address_pos = get_street_head_positions(header)
append_headings(header, csv_writer_object)
status_pos = header.index('Status')
image_location_pos = header.index('Street View Image Location')

cnt = 0

print("\n\n--------------------------------------------------")
print("Data Processing\n")
time.sleep(SLEEP_TIME)

for row in csv_reader_object:
    print("--------------------------------------------------")

    # curren data
    total_data = row
    cnt += 1

    # is_blank = check_blank_row(
    #     row, cnt, status_pos, csv_writer_object, address_pos)
    # if is_blank == True:
    #     print("BLANK")
    #     print(is_blank)
    #     continue



    full_address = get_full_address_from_heading_pos(row, address_pos)
    print(f"#{cnt}: {full_address}")

    print("get street view data")
    # get street view data
    street_view_data = extract_street_view_metadata(full_address)
    if street_view_data == None:
        print("STREETVIEWDATA NONE")
        print(street_view_data)
        error_row(cnt, total_data, status_pos, csv_writer_object, image_location_pos)
        continue

    # get status metadata
    print("get status metadata")
    status = street_view_data['status']
    total_data.append(status)

    # get image data
    print("get image_data")
    image_data = metadata_processor(full_address, status)
    print("before if image_date == None")
    if image_data == None:
        print("IMAGE DATA NONE")
        print(image_data)
        error_row(cnt, total_data, status_pos, csv_writer_object, image_location_pos)
        continue

    try:
        # downloaded_url = image_data[0]
        google_img_url = image_data[0]
        gdrive_location = image_data[1]
    except:
        error_row(cnt, total_data, status_pos, csv_writer_object, image_location_pos)
        continue

    print("total_data.append(downloaded_url)")
    # total_data.append(downloaded_url)
    total_data.append(google_img_url)
    total_data.append(gdrive_location)

    if INCLUDE_SATELLITE_VIEW == True:
      # get satellite image
      satellite_url = ""
      satellite_location = ""
      satellite_data = get_satellite_image_url(full_address)
      satellite_url = satellite_data[0]
      satellite_location = satellite_data[1]

      total_data.append(satellite_url)
      total_data.append(satellite_location)

    print("\n" * 2)

    # save row
    csv_writer_object.writerow(total_data)

print("end")

src_file.close()
des_file.close()
