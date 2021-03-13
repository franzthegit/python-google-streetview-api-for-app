import os
import sys
import time
from constants import APPEND_HEADERS, ADDRESS_INF_HEADERS, SLEEP_TIME, GDRIVE_DEFAULT_IMAGE

def check_blank_row(row, cnt, status_pos, writer, address_pos):
    # checking blank row
    is_blank_row = False
    for pos in address_pos:
        if not row[pos]:
            is_blank_row = True
            break

    if is_blank_row == True:
        print(
            f"Incomplete Address, Please check again {cnt + 1} th row in the origin CSV data...\n\n\n")
        row.insert(status_pos, 'ERROR')
        writer.writerow(row)
        time.sleep(SLEEP_TIME)

    return is_blank_row


def get_full_address_from_heading_pos(row, address_pos):
    address = []

    # get address
    for col in address_pos:
        address.append(row[col])

    # full joined address
    full_address = ', '.join(address)
    return full_address


def get_street_head_positions(header):
    positions = []
    missing_headers = []

    print("--------------------------------------------------")
    print("Checking Address Information Headings...\n")
    time.sleep(SLEEP_TIME)

    for idx, head_item in enumerate(ADDRESS_INF_HEADERS):
        print(f"No {idx + 1}: checking '{head_item}'")
        time.sleep(SLEEP_TIME)

        pos = idx + 1
        try:
            pos = header.index(head_item)
            print(f"Column: {pos}(0 based index)\n")
        except ValueError:
            missing_headers.append(f'"{head_item}"')
            print(
                f"Error, Please check if there is {head_item} heading in the first row\n")
            pass
        positions.append(pos)

    if len(missing_headers) != 0:
        sys.exit(f"Column Missing Error: {', '.join(missing_headers)}\nExiting...")
    print(f"address information headings indexes: {positions}\n\n")
    return positions


def append_headings(header, writer):
    print("--------------------------------------------------")
    print("Appending Header Columns to the origin\n")
    time.sleep(SLEEP_TIME)

    for head_item in APPEND_HEADERS:
        if head_item not in header:
            print(f"appending '{head_item}'")
            time.sleep(SLEEP_TIME)
            header.append(head_item)
    writer.writerow(header)

def error_row(row_cnt, data, status_pos, writer, image_location_pos):
    data[status_pos] = "ERROR"
    # data[image_location_pos] = GDRIVE_DEFAULT_IMAGE
    data.append(GDRIVE_DEFAULT_IMAGE)
    data.append("")
    data.append(GDRIVE_DEFAULT_IMAGE)
    print(
        f"Error Cannot get addresses, Please check again {row_cnt + 1} th row in the origin CSV data...\n\n\n")
