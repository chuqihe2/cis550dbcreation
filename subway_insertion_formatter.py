import csv
import os

from files import *
from neo4j.v1 import GraphDatabase, basic_auth

with open(cleaned_data_path(SUBWAY), newline='', mode='r') as in_file, \
        open(sql_path(SUBWAY), newline='', mode='w') as out_file:
    reader = csv.DictReader(in_file)
    lines = set()  # All lines already created.
    driver = GraphDatabase.driver("bolt://hobby-dhgbijnckhclgbkeccgcoial.dbs.graphenedb.com:24786",
                                  auth=basic_auth(os.environ['DBUSER'], os.environ['DBPSWD']))
    session = driver.session()

    def execute_and_write_out(query):
        session.run(query)
        out_file.write(query)

    # Clear old records first
    execute_and_write_out("MATCH (n)\nDETACH DELETE n;\n")

    # Write out is a back-upl Queries are sent to server directly.
    for record in reader:
        execute_and_write_out('CREATE (s:Station {{ name: \'{name}\', ' \
                              'longitude: {longitude}, ' \
                              'latitude: {latitude} }});\n'.format_map(
            {'name': record['Station'].replace("'", "\\'"),
             'longitude': record['Longitude'],
             'latitude': record['Latitude']}))

        for line in eval(record['Line']):
            if line not in lines:
                lines.add(line)
                execute_and_write_out(
                    'CREATE (l:Line {{ name: \'{0}\'}});\n'.format(line))
            execute_and_write_out(
                'MATCH (s:Station),(l:Line)\n'
                'WHERE s.name = \'{station_name}\' AND l.name = \'{line_name}\'\n'
                'CREATE (l)-[r:GOTO]->(s);\n'.format_map(
                    {
                        'station_name': record['Station'],
                        'line_name': line
                    }))

session.close()
