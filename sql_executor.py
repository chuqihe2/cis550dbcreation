import csv
import datetime
import mysql.connector
import os
import time

from files import *

config = {
    'user': os.environ['CIS550USERNAME'],
    'password': os.environ['CIS550PASSWORD'],
    'host': 'timesquaredata.cduvdiu5r6xm.us-east-2.rds.amazonaws.com',
    'port': 3306,
    'database': 'tsdata',
    'raise_on_warnings': True,
}

# Shared DB connection
cnx = mysql.connector.connect(**config)


def insert_as_records(file_name, table_name, schema, keys):
    """
    Inserts all records in the CSV file as records into the specified table.
    :param file_name: File name. This will be used as both input file name and output file name (under different dir).
    :param table_name: Name of the target table.
    :param schema: A map from field names to field types.
    :param keys: A list of key fields' names. They will always be included.
    """

    def format_value(value, field_type):
        """
        Format the value correctly so that it is ready for SQL formatting.
        """
        if field_type == 'date':
            return datetime.datetime.strptime(value, "%m/%d/%Y")
        else:
            return value

    # Make it a set for faster lookup
    keys = set(keys)

    start_time = time.process_time()
    print("Formatting {0} as SQL insertions into {1}.".format(file_name, table_name))

    cursor = cnx.cursor(buffered=True)
    cursor.execute("TRUNCATE TABLE {0};".format(table_name))

    inserted = 0
    dropped = 0
    with open(cleaned_data_path(file_name), newline='', mode='r') as in_file:
        reader = csv.DictReader(in_file)
        for record in reader:
            included_fields = [field for field in record if len(record[field]) > 0 or field in keys]
            query_template = 'REPLACE INTO {table_name} ({schema_def}) VALUES ({values});\n'.format_map({
                'table_name': table_name,
                'schema_def': ', '.join(included_fields),
                'values': ', '.join(['%({0})s'.format(field) for field in included_fields])
            })
            try:
                cursor.execute(query_template,
                               {field: format_value(record.get(field), schema[field]) for field in record})
            except mysql.connector.Error as err:
                print(
                    'Exception when inserting {0}-th record:\n{1}Warning:{2}'.format(inserted + 1, record, err))
                dropped += 1
            except mysql.connector.Warning as warning:
                print('Warning when inserting {0}-th record:\n{1}Warning:{2}'.format(inserted + 1, record, warning))
                inserted += 1
            else:
                inserted += 1

    cnx.commit()

    print("Done inserting {0} records into {1} in {2} second(s)! {3} were dropped!"
          .format(inserted, file_name,
                  time.process_time() - start_time,
                  dropped))


insert_as_records(FOOD, 'Food', {
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

insert_as_records(ENTERTAINMENT, 'Entertainment', {
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

insert_as_records(HOTELS, 'Hotel', {
    'StreetName': 'varchar',
    'Building': 'number',
    'Name': 'varchar',
    'ZipCode': 'varchar',
    'Longitude': 'number',
    'Latitude': 'number',
    'PhoneNumber': 'varchar',
    'WebSite': 'varchar'
}, ['StreetName', 'Building', 'Name'])

insert_as_records(SIGNAGE, 'Signage', {
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

insert_as_records(REST_INSPECTIONS, 'InspectionResult', {
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

insert_as_records(COLLISIONS, 'TrafficAccident', {
    'OnStreet': 'varchar',
    'CrossStreet': 'varchar',
    'PedestrianInjured': 'number',
    'PedestrianKilled': 'number',
    'CyclistInjured': 'number',
    'CyclistKilled': 'number',
    'MotoristInjured': 'number',
    'MotoristKilled': 'number',
}, [])

# Close the connection
cnx.close()
