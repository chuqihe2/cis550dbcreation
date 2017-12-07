import csv
import pprint
import re

from files import *
from functools import reduce

geom_re = re.compile('^POINT \((-?\d+\.?\d*?) (-?\d+\.?\d*?)\)$')


def get_lon_and_lat(raw_point):
    """
    Parses the longitude+latitude tuple and return the values in this order.
    """
    match = geom_re.search(raw_point)
    return float(match.group(1)), float(match.group(2))


def clean_line_symbol(line):
    """
    Cleans weird subway line format. E.g. 1 as 2001.
    """
    if line.startswith('200'):
        return line[3:].upper().strip()
    return line.upper().strip()


def get_lines(all_lines):
    """
    Takes a raw string of the form S1-S2-...-Sn and returns all each elements in a set.
    """
    return set(map(clean_line_symbol, all_lines.split('-')))


def get_station_name(entrance_name):
    """
    Strip off entrance-specific information. E.g. SE corner.
    """
    at_index = str(entrance_name).rfind(' at ')
    if at_index == -1:
        return entrance_name.strip()
    return entrance_name[:at_index].strip()


with open(input_data_path(SUBWAY), newline='', mode='r') as in_file, \
        open(cleaned_data_path(SUBWAY), newline='', mode='w') as out_file:
    reader = csv.DictReader(in_file)
    pprint.pprint(reader.fieldnames)

    # Pre-process all records before batch-cleaning
    name_to_records = dict()
    for record in reader:
        name = get_station_name(record['NAME'])
        if len(name) == 0:
            # Skip invalid names
            continue
        lon, lat = get_lon_and_lat(record['the_geom'])
        lines = get_lines(record['LINE'])
        if name not in name_to_records:
            name_to_records[name] = []
        name_to_records[name].append({
            'Station': name,
            'Longitude': lon,
            'Latitude': lat,
            'Line': lines})

    # Write a record with the union of all lines, and the average of all geo coordinates.
    # This is only a backup. Queries are sent to the server directly.
    writer = csv.DictWriter(out_file,
                            fieldnames=['Station', 'Longitude', 'Latitude', 'Line'])
    writer.writeheader()
    for name in sorted(name_to_records):
        all_records = name_to_records[name]
        writer.writerow({
            'Station': name,
            'Longitude': sum(map(lambda r: r['Longitude'], all_records)) / len(all_records),
            'Latitude': sum(map(lambda r: r['Latitude'], all_records)) / len(all_records),
            'Line': repr(reduce(lambda acc, r2: acc | r2['Line'], all_records, set()))})
