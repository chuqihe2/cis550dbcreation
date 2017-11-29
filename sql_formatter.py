"""
DEPRECATED: This is for the old Oracle DB instance, which is replaced by a MySQL DB instance.
Use sql_executor instead.
"""
import csv
import time
from collections import OrderedDict

from files import *

type_to_format_fn = {
    'varchar': lambda val: "'{0}'".format(escape(val)),
    'number': str,
    'date': lambda val: "TO_DATE('{0}', 'MM/DD/YYYY')".format(escape(val))
}


def escape(str_value):
    return str_value.replace('\'', '\'\'')


def format_sql(table_name, schema, keys, record):
    """
    Formats the given record into a SQL query that inserts it into the table.
    :param table_name: Name of the target table as string.
    :param schema: A map from field names to field types.
    :param keys: A list of key fields' names. They will always be included.
    :param record: A OrderedDict from field names to values.
    """
    record = OrderedDict(sorted([item for item in record.items() if len(item[1]) > 0 or item[0] in keys]))
    schema_def = ','.join([
        field_name for field_name in record
    ])
    values = ','.join([
        type_to_format_fn[schema[field_name]](value) for field_name, value in record.items()
    ])
    return 'INSERT INTO {table_name} ({schema_def}) VALUES ({values});\n'.format_map({
        'table_name': table_name,
        'schema_def': schema_def,
        'values': values
    })


def format_file(file_name, table_name, schema, keys):
    """
    Formats all records in the given file into SQL insertion queries.
    :param file_name: File name. This will be used as both input file name and output file name (under different dir).
    :param table_name: Name of the target table.
    :param schema: A map from field names to field types.
    :param keys: A list of key fields' names. They will always be included.
    """
    start_time = time.process_time()
    print("Formatting {0} as SQL insertions into {1}.".format(file_name, table_name))
    with open(cleaned_data_path(file_name), newline='', mode='r') as in_file, \
            open(sql_path(file_name), newline='', mode='w') as out_file:
        reader = csv.DictReader(in_file)
        out_file.write("SET DEFINE OFF;\nTRUNCATE TABLE {0};\n".format(table_name))
        for record in reader:
            out_file.write(format_sql(table_name, schema, keys, record))
    print("Done formatting {0} in {1} second(s)!".format(file_name, time.process_time() - start_time))


format_file(FOOD, 'Food', {
    'StreetName': 'varchar',
    'Building': 'number',
    'Name': 'varchar',
    'ZipCode': 'varchar',
    'Longitude': 'number',
    'Latitude': 'number',
    'PhoneNumber': 'varchar',
    'WebSite': 'varchar',
    'Cuisine': 'varchar'
}, ['StreetName', 'Building', 'Name'])

format_file(ENTERTAINMENT, 'Entertainment', {
    'StreetName': 'varchar',
    'Building': 'number',
    'Name': 'varchar',
    'ZipCode': 'varchar',
    'Longitude': 'number',
    'Latitude': 'number',
    'PhoneNumber': 'varchar',
    'WebSite': 'varchar',
    'Type': 'varchar'
}, ['StreetName', 'Building', 'Name'])

format_file(HOTELS, 'Hotel', {
    'StreetName': 'varchar',
    'Building': 'number',
    'Name': 'varchar',
    'ZipCode': 'varchar',
    'Longitude': 'number',
    'Latitude': 'number',
    'PhoneNumber': 'varchar',
    'WebSite': 'varchar'
}, ['StreetName', 'Building', 'Name'])

format_file(SIGNAGE, 'Signage', {
    'StreetName': 'varchar',
    'Building': 'number',
    'BuildingName': 'varchar',
    'Name': 'varchar',
    'NumberOfScreens': 'number',
    'Height': 'varchar',
    'Type': 'varchar',
    'Orientation': 'varchar',
    'Area': 'number',
}, ['StreetName', 'Building', 'BuildingName', 'Name'])

format_file(REST_INSPECTIONS, 'InspectionResult', {
    'StreetName': 'varchar',
    'Building': 'number',
    'Name': 'varchar',
    'InspectionDate': 'date',
    'ViolationCode': 'varchar',
    'Description': 'varchar',
    'CriticalFlag': 'varchar',
    'Score': 'number',
    'Grade': 'varchar',
    'Type': 'varchar',
}, ['StreetName', 'Building', 'Name', 'InspectionDate', 'ViolationCode'])

format_file(COLLISIONS, 'TrafficAccident', {
    'OnStreet': 'varchar',
    'CrossStreet': 'varchar',
    'PedestrianInjured': 'number',
    'PedestrianKilled': 'number',
    'CyclistInjured': 'number',
    'CyclistKilled': 'number',
    'MotoristInjured': 'number',
    'MotoristKilled': 'number',
}, [])
