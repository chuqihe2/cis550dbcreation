import csv

from files import *

with open(cleaned_data_path(SUBWAY), newline='', mode='r') as in_file, \
        open(sql_path(SUBWAY), newline='', mode='w') as out_file:
    reader = csv.DictReader(in_file)
    lines = set()  # All lines already created.

    for record in reader:
        out_file.write(
            'CREATE (s:Station {{ name: \'{name}\', '
            'longitude: {longitude}, '
            'latitude: {latitude} }});\n'.format_map(
                {
                    'name': record['Station'],
                    'longitude': record['Longitude'],
                    'latitude': record['Latitude']
                }))
        for line in eval(record['Line']):
            if line not in lines:
                lines.add(line)
                out_file.write(
                    'CREATE (l:Line {{ name: \'{0}\'}});\n'.format(line))
            out_file.write(
                'MATCH (s:Station),(l:Line)\n'
                'WHERE s.name = \'{station_name}\' AND l.name = \'{line_name}\'\n'
                'CREATE (l)-[r:GOTO]->(s);\n'.format_map(
                    {
                        'station_name': record['Station'],
                        'line_name': line
                    }))
