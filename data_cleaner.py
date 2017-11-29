"""
Converts data to table schema, in CSV format.
"""

import csv
import pprint
import re
import time
import usaddress

from files import *


# =========================================================
# ================ STRING-LEVEL CLEANING ==================
# =========================================================

def clean_str(s):
    return s.strip('"\' ,').lower()


# =========================================================
# ================ STREET ADDRESS PARSER ==================
# =========================================================

def get_first_numeric_part(str_value):
    numeric_re = re.compile("(\d+)")
    numeric_match = numeric_re.match(str_value)
    if numeric_match:
        return numeric_match.group(0)
    return None


def standardize_street_name(street_name):
    # Match the Arabic-numerical representations
    street_name = street_name.lower()
    numeric_street_name = get_first_numeric_part(street_name)
    if numeric_street_name is not None:
        return numeric_street_name
    # Match the English representations
    if 'first' in street_name or 'one' in street_name:
        return '1'
    if 'second' in street_name or 'two' in street_name:
        return '2'
    if 'third' in street_name or 'three' in street_name:
        return '3'
    if 'fourth' in street_name or 'four' in street_name:
        return '4'
    if 'fifth' in street_name or 'five' in street_name:
        return '5'
    if 'sixth' in street_name or 'six' in street_name:
        return '6'
    if 'seventh' in street_name or 'seven' in street_name:
        return '7'
    if 'eighth' in street_name or 'eight' in street_name:
        return '8'
    if 'ninth' in street_name or 'nine' in street_name:
        return '9'
    if 'tenth' in street_name or 'ten' in street_name:
        return '10'
    if 'eleventh' in street_name or 'eleven' in street_name:
        return '11'
    if 'twelfth' in street_name or 'twelve' in street_name:
        return '12'
    return street_name


def standardize_street_post_type(st_post_type):
    st_post_type = st_post_type.lower()
    # Use abbreviations
    if st_post_type == 'street' or st_post_type == 'str' or st_post_type == 'st.' or st_post_type == 'str.':
        st_post_type = 'st'
    elif st_post_type == 'avenue' or st_post_type == 'ave.':
        st_post_type = 'ave'
    elif st_post_type == 'square' or st_post_type == 'sq.':
        st_post_type = 'sq'
    elif st_post_type == 'court' or st_post_type == 'ct.':
        st_post_type = 'ct'
    return clean_str(st_post_type)


def parse_street_address(st_addr):
    st_addr = clean_str(st_addr)
    # Whitelisted records to enable manual parsing.
    if len(st_addr) == 0:
        return {}
    if st_addr == 'military island':
        return {'StreetName': st_addr, 'AddressNumber': 0}
    if st_addr == '7 times square tower':
        # Malformed address: strip of the suffix tower.
        st_addr = '7 times square'

    token_dict = dict([(pair[1], clean_str(pair[0]))
                       for pair in usaddress.parse(st_addr)])

    # Auto-parse the address string
    std_st_name = standardize_street_name(token_dict['StreetName'])
    if 'StreetNamePostType' in token_dict:
        token_dict['StreetName'] = '{0} {1}'.format(std_st_name,
                                                    standardize_street_post_type(token_dict['StreetNamePostType']))
    else:
        token_dict['StreetName'] = std_st_name

    # Standardize building numbers
    building_number = get_first_numeric_part(token_dict['AddressNumber'])
    if building_number is None:
        token_dict['AddressNumber'] = '0'
    else:
        token_dict['AddressNumber'] = building_number

    return token_dict


# =========================================================
# ======================== FOOD ===========================
# =========================================================

dropped_examples = 0
start_time = time.process_time()
print("Processing food")
with open(input_data_path(FOOD), newline='', mode='r') as in_file, \
        open(cleaned_data_path(FOOD), newline='', mode='w') as out_file:
    reader = csv.DictReader(in_file)
    pprint.pprint(reader.fieldnames)
    writer = csv.DictWriter(out_file,
                            fieldnames=['StreetName', 'Building', 'Name', 'ZipCode', 'Longitude', 'Latitude',
                                        'PhoneNumber', 'WebSite', 'Cuisine'])
    writer.writeheader()
    for record in reader:
        try:
            address = parse_street_address(record['Address'])
            writer.writerow({
                'StreetName': address['StreetName'],
                'Building': address['AddressNumber'],
                'Name': clean_str(record['Company Name']),
                'ZipCode': clean_str(record['Postcode']),
                'Longitude': clean_str(record['Longitude']),
                'Latitude': clean_str(record['Latitude']),
                'PhoneNumber': clean_str(record['Phone']),
                'WebSite': clean_str(record['Website']),
                'Cuisine': clean_str(
                    record['Sub Subindustry'] if 'Sub Subindustry' in record else record['Subindustry']),
            })
        except Exception as e:
            dropped_examples += 1
            print('Dropped example: {0}.\nReason: {1}'.format(pprint.pformat(record), e))
print("Done processing food in {0} second(s)! Dropped {1} examples.".format(time.process_time() - start_time,
                                                                            dropped_examples))

# =========================================================
# ==================== ENTERTAINMENT ======================
# =========================================================

dropped_examples = 0
start_time = time.process_time()
print("Processing entertainments")
with open(input_data_path(ENTERTAINMENT), newline='', mode='r') as in_file, \
        open(cleaned_data_path(ENTERTAINMENT), newline='', mode='w') as out_file:
    reader = csv.DictReader(in_file)
    pprint.pprint(reader.fieldnames)
    writer = csv.DictWriter(out_file,
                            fieldnames=['StreetName', 'Building', 'Name', 'ZipCode', 'Longitude', 'Latitude',
                                        'PhoneNumber', 'WebSite', 'Type'])
    writer.writeheader()
    for record in reader:
        try:
            address = parse_street_address(record['Address'])
            writer.writerow({
                'StreetName': address['StreetName'],
                'Building': address['AddressNumber'],
                'Name': clean_str(record['Company Name']),
                'ZipCode': clean_str(record['Postcode']),
                'Longitude': clean_str(record['Longitude']),
                'Latitude': clean_str(record['Latitude']),
                'PhoneNumber': clean_str(record['Phone']),
                'WebSite': clean_str(record['Website']),
                'Type': clean_str(record['Subindustry']),
            })
        except Exception as e:
            dropped_examples += 1
            print('Dropped example: {0}.\nReason: {1}'.format(pprint.pformat(record), e))
print("Done processing entertainments in {0} second(s)! Dropped {1} examples.".format(time.process_time() - start_time,
                                                                                      dropped_examples))

# =========================================================
# ======================= HOTELS ==========================
# =========================================================

start_time = time.process_time()
print("Processing hotels")
with open(input_data_path(HOTELS), newline='', mode='r') as in_file, \
        open(cleaned_data_path(HOTELS), newline='', mode='w') as out_file:
    reader = csv.DictReader(in_file)
    pprint.pprint(reader.fieldnames)
    writer = csv.DictWriter(out_file,
                            fieldnames=['StreetName', 'Building', 'Name', 'ZipCode', 'Longitude', 'Latitude',
                                        'PhoneNumber', 'WebSite'])
    writer.writeheader()
    for record in reader:
        try:
            address = parse_street_address(record['Address'])
            writer.writerow({
                'StreetName': address['StreetName'],
                'Building': address['AddressNumber'],
                'Name': clean_str(record['Company Name']),
                'ZipCode': clean_str(record['Postcode']),
                'Longitude': clean_str(record['Longitude']),
                'Latitude': clean_str(record['Latitude']),
                'PhoneNumber': clean_str(record['Phone']),
                'WebSite': clean_str(record['Website']),
            })
        except Exception as e:
            dropped_examples += 1
            print('Dropped example: {0}.\nReason: {1}'.format(pprint.pformat(record), e))
print("Done processing hotels in {0} second(s)! Dropped {1} examples.".format(time.process_time() - start_time,
                                                                              dropped_examples))

# =========================================================
# ======================= SIGNAGE =========================
# =========================================================

dropped_examples = 0
start_time = time.process_time()
print("Processing signage")
with open(input_data_path(SIGNAGE), newline='', mode='r') as in_file, \
        open(cleaned_data_path(SIGNAGE), newline='', mode='w') as out_file:
    reader = csv.DictReader(in_file)
    pprint.pprint(reader.fieldnames)
    writer = csv.DictWriter(out_file,
                            fieldnames=['StreetName', 'Building', 'BuildingName', 'Name', 'NumberOfScreens', 'Height',
                                        'Type', 'Orientation', 'Area'])
    writer.writeheader()
    for record in reader:
        try:
            address = parse_street_address(record['Building Address'])
            writer.writerow({
                'StreetName': address['StreetName'],
                'Building': address['AddressNumber'],
                'BuildingName': clean_str(record['Location Description'] if len(record['Location Description']) > 0
                                          else 'None'),
                'Name': clean_str(record['Screen Name (LED + Vinyl Signs)']),
                'NumberOfScreens': clean_str(record['#']),
                'Height': clean_str(record['Height']),
                'Type': clean_str(record['Type']),
                'Orientation': clean_str(record['Location Description']),
                'Area': clean_str(record['SF']),
            })
        except Exception as e:
            dropped_examples += 1
            print('Dropped example: {0}.\nReason: {1}'.format(pprint.pformat(record), e))
print("Done processing hotels in {0} second(s)! Dropped {1} examples.".format(time.process_time() - start_time,
                                                                              dropped_examples))

# =========================================================
# ================ RESTAURANT INSPECTION ==================
# =========================================================

dropped_examples = 0
start_time = time.process_time()
print("Processing restaurant inspections")
with open(input_data_path(REST_INSPECTIONS), newline='', mode='r') as in_file, \
        open(cleaned_data_path(REST_INSPECTIONS), newline='', mode='w') as out_file:
    reader = csv.DictReader(in_file)
    pprint.pprint(reader.fieldnames)
    writer = csv.DictWriter(out_file,
                            fieldnames=['StreetName', 'Building', 'Name', 'InspectionDate', 'ViolationCode',
                                        'Description', 'CriticalFlag', 'Score', 'Grade', 'Type'])
    writer.writeheader()
    for record in reader:
        try:
            address = parse_street_address('{0} {1}'.format(record['BUILDING'], record['STREET']))
            writer.writerow({
                'StreetName': address['StreetName'],
                'Building': address['AddressNumber'],
                'Name': clean_str(record['DBA']),
                'InspectionDate': clean_str(record['INSPECTION DATE']),
                'ViolationCode': clean_str(record['VIOLATION CODE']) \
                    if 'VIOLATION CODE' in record and len(record['VIOLATION CODE']) > 0 else 'NONE',
                'Description': clean_str(record['VIOLATION DESCRIPTION']),
                'CriticalFlag': clean_str(record['CRITICAL FLAG']),
                'Score': clean_str(record['SCORE']),
                'Grade': clean_str(record['GRADE']),
                'Type': clean_str(record['INSPECTION TYPE']),
            })
        except Exception as e:
            dropped_examples += 1
            print('Dropped example: {0}.\nReason: {1}'.format(pprint.pformat(record), e))
print("Done processing restaurant inspections in {0} second(s)! Dropped {1} examples.".format(
    time.process_time() - start_time, dropped_examples))

# =========================================================
# ================ RESTAURANT INSPECTION ==================
# =========================================================

dropped_examples = 0
start_time = time.process_time()
print("Processing collisions logs")
with open(input_data_path(COLLISIONS), newline='', mode='r') as in_file, \
        open(cleaned_data_path(COLLISIONS), newline='', mode='w') as out_file:
    reader = csv.DictReader(in_file)
    pprint.pprint(reader.fieldnames)
    writer = csv.DictWriter(out_file,
                            fieldnames=['OnStreet', 'CrossStreet', 'PedestrianInjured', 'PedestrianKilled',
                                        'CyclistInjured', 'CyclistKilled', 'MotoristInjured', 'MotoristKilled'])
    writer.writeheader()
    for record in reader:
        try:
            on_st = parse_street_address(record['ON STREET NAME'])
            crs_st = parse_street_address(record['CROSS STREET NAME'])
            off_st = parse_street_address(record['OFF STREET NAME'])
            writer.writerow({
                'OnStreet': on_st['StreetName'] if 'StreetName' in on_st \
                    else off_st['StreetName'],
                'CrossStreet': crs_st['StreetName'] if 'StreetName' in crs_st \
                    else '',
                'PedestrianInjured': clean_str(record['NUMBER OF PEDESTRIANS INJURED']),
                'PedestrianKilled': clean_str(record['NUMBER OF PEDESTRIANS KILLED']),
                'CyclistInjured': clean_str(record['NUMBER OF CYCLIST INJURED']),
                'CyclistKilled': clean_str(record['NUMBER OF CYCLIST KILLED']),
                'MotoristInjured': clean_str(record['NUMBER OF MOTORIST INJURED']),
                'MotoristKilled': clean_str(record['NUMBER OF MOTORIST KILLED']),
            })
        except Exception as e:
            dropped_examples += 1
            # As this data is way too large, and standardization of street names strips off most irrelevant records,
            # do not print each dropped example out.
            # print('Dropped example: {0}.\nReason: {1}'.format(pprint.pformat(record), str(e)))
print("Done processing collision logs inspections in {0} second(s)! Dropped {1} examples.".format(
    time.process_time() - start_time, dropped_examples))
