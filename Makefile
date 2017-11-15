cleaner = data_cleaner.py
sql_formatter = sql_formatter.py
aws_rds_db = '${CIS550USERNAME}/${CIS550PASSWORD}@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=time-square-data.cduvdiu5r6xm.us-east-2.rds.amazonaws.com)(PORT=1521))(CONNECT_DATA=(SID=TSDATA)))'

INSPECTION = DOHMH_New_York_City_Restaurant_Inspection_Results
COLLISION = NYPD_Motor_Vehicle_Collisions
ENTERTAINMENT = Times_Square_Entertainment_Venues
FOOD = Times_Square_Food___Beverage_Locations
HOTEL = Times_Square_Hotels
SIGNAGE = Times_Square_Signage

all_data: inspection collision entertainment food hotel signage

clean_data:
	python3 $(cleaner)

cleaned/$(INSPECTION).csv: clean_data

cleaned/$(COLLISION).csv: clean_data

cleaned/$(ENTERTAINMENT).csv: clean_data

cleaned/$(FOOD).csv: clean_data

cleaned/$(HOTEL).csv: clean_data

cleaned/$(SIGNAGE).csv: clean_data


format_sql: cleaned/$(INSPECTION).csv cleaned/$(COLLISION).csv cleaned/$(ENTERTAINMENT).csv cleaned/$(FOOD).csv cleaned/$(HOTEL).csv cleaned/$(SIGNAGE).csv
	python3 $(sql_formatter)

sql/$(INSPECTION).sql: format_sql

sql/$(COLLISION).sql: format_sql

sql/$(ENTERTAINMENT).sql: format_sql

sql/$(FOOD).sql: format_sql

sql/$(HOTEL).sql: format_sql

sql/$(SIGNAGE).sql: format_sql


inspection: sql/$(INSPECTION).sql
	sqlplus64 $(aws_rds_db) < sql/$(INSPECTION).sql

collision: sql/$(COLLISION).sql
	sqlplus64 $(aws_rds_db) < sql/$(COLLISION).sql

entertainment: sql/$(ENTERTAINMENT).sql
	sqlplus64 $(aws_rds_db) < sql/$(ENTERTAINMENT).sql

food: sql/$(FOOD).sql
	sqlplus64 $(aws_rds_db) < sql/$(FOOD).sql

hotel: sql/$(HOTEL).sql
	sqlplus64 $(aws_rds_db) < sql/$(HOTEL).sql

signage: sql/$(SIGNAGE).sql
	sqlplus64 $(aws_rds_db) < sql/$(SIGNAGE).sql
