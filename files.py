"""
File paths and their utilities.
"""


def input_data_path(filename):
    return '{0}/{1}.csv'.format(DATA_DIR, filename)


def cleaned_data_path(filename):
    return '{0}/{1}.csv'.format(CLEANED_DIR, filename)


def sql_path(filename):
    return '{0}/{1}.sql'.format(SQL_DIR, filename)


DATA_DIR = 'data'
CLEANED_DIR = 'cleaned'
SQL_DIR = 'sql'

# Uses (BUILDING,STREET)
REST_INSPECTIONS = 'DOHMH_New_York_City_Restaurant_Inspection_Results'

# Uses (LOCATION), also (ON STREET NAME,CROSS STREET NAME,OFF STREET NAME)
COLLISIONS = 'NYPD_Motor_Vehicle_Collisions'

# Uses (Address)
ENTERTAINMENT = 'Times_Square_Entertainment_Venues'
FOOD = 'Times_Square_Food___Beverage_Locations'
HOTELS = 'Times_Square_Hotels'

# Uses (Building Address)
SIGNAGE = 'Times_Square_Signage'

# NYC Subway data (all entrances)
SUBWAY = 'DOITT_SUBWAY_ENTRANCE_01_13SEPT2010'

# Table creation script
TABLE_CREATION = sql_path('table_creation')