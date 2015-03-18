from collectData import *
import pymysql


list_of_tables = ['B19001', 'B08303']

states = {"Mississippi": 28, "Oklahoma": 40, "Delaware": 10, "Minnesota": 27, "Illinois": 17, "Arkansas": "05", 
"New Mexico": 35, "Indiana": 18, "Maryland": 24, "Louisiana": 22, "Idaho": 16, "Wyoming": 56, 
"Tennessee": 47, "Arizona": "04", "Iowa": 19, "Michigan": 26, "Kansas": 20, "Utah": 49, 
"Virginia": 51, "Oregon": 41, "Connecticut": "09",  "Montana": 30, "California": "06", "Massachusetts": 25, 
"West Virginia": 54, "South Carolina": 45, "New Hampshire": 33, "Wisconsin": 55, "Vermont": 50, 
"Georgia": 13, "North Dakota": 38, "Pennsylvania": 42, "Florida": 12, "Alaska": "02", "Kentucky": 21, 
"Hawaii": 15, "Nebraska": 31, "Missouri": 29, "Ohio": 39, "Alabama": "01", "New York": 36, "South Dakota": 46, 
"Colorado": "08", "New Jersey": 34, "Washington": 53, "North Carolina": 37, "District of Columbia": 11, 
"Texas": 48, "Nevada": 32, "Maine": 23, "Rhode Island": 44}

dbname="acs_survey2"
host="localhost"
user="root"
passwd=""
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

# c = db.cursor()
# create_columninfo = """CREATE TABLE IF NOT EXISTS column_info ( 
#          ACScolumnId VARCHAR (128),
#          columnName VARCHAR (128),
#          ACStableId VARCHAR (255),
#          tableName VARCHAR (128),
#          denom VARCHAR (128)
#          )
#        ENGINE=MyISAM DEFAULT CHARSET=utf8"""
# c.execute(create_columninfo)

# insertCol = '''INSERT INTO column_info (ACScolumnId, columnName, ACStableId, tableName, denom) VALUES (%s, %s, %s, %s, %s)'''

# for table in list_of_tables:
# 	c.executemany(insertCol, fetchTableInfo(table))
# c.close()

c=db.cursor()

# create_income = """CREATE TABLE IF NOT EXISTS income (
# 	geoID VARCHAR (128),
# 	Fips VARCHAR (128),
# 	B19001001 VARCHAR(128),
# 	B19001002 VARCHAR(128), 
# 	B19001003 VARCHAR(128), 
# 	B19001004 VARCHAR(128),
# 	B19001005 VARCHAR(128),  
# 	B19001006 VARCHAR(128),
# 	B19001007 VARCHAR(128),  
# 	B19001008 VARCHAR(128), 
# 	B19001009 VARCHAR(128), 
# 	B19001010 VARCHAR(128), 
# 	B19001011 VARCHAR(128), 
# 	B19001012 VARCHAR(128), 
# 	B19001013 VARCHAR(128), 
# 	B19001014 VARCHAR(128), 
# 	B19001015 VARCHAR(128), 
# 	B19001016 VARCHAR(128), 
# 	B19001017 VARCHAR(128)
#          ) ENGINE=MyISAM DEFAULT CHARSET=utf8"""

# c.execute(create_income)
# print "created income chart"



# for state in states.keys():
# 	print "starting state" + state
# 	insertIncome = '''INSERT INTO income (geoID, Fips, B19001001, B19001002, B19001003, B19001004, B19001005, 
# 		B19001006, B19001007, B19001008, B19001009, B19001010, B19001011, B19001012, B19001013, 
# 		B19001014, B19001015, B19001016, B19001017) VALUES 
# 		(%s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
# 	c.executemany(insertIncome, downloadTableData("B19001", state))
# 	print "finished state" + state


create_commute = """CREATE TABLE IF NOT EXISTS commute (
	geoID VARCHAR (128),
	Fips VARCHAR (128),
	B08303001 VARCHAR(128),
	B08303002 VARCHAR(128), 
	B08303003 VARCHAR(128), 
	B08303004 VARCHAR(128),
	B08303005 VARCHAR(128),  
	B08303006 VARCHAR(128),
	B08303007 VARCHAR(128),  
	B08303008 VARCHAR(128), 
	B08303009 VARCHAR(128), 
	B08303010 VARCHAR(128), 
	B08303011 VARCHAR(128), 
	B08303012 VARCHAR(128), 
	B08303013 VARCHAR(128)
         ) ENGINE=MyISAM DEFAULT CHARSET=utf8"""

c.execute(create_commute)
print "created COMMUTE chart"

for state in states.keys():
	print "starting state" + state
	insertCommute = '''INSERT INTO commute (geoID, Fips, B08303001, B08303002, B08303003, B08303004, 
		B08303005, B08303006, B08303007, B08303008, B08303009, B08303010, B08303011, 
		B08303012, B08303013) VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s)''' 
	c.executemany(insertCommute, downloadTableData("B08303", state))
	print "finished state" + state
db.commit()
c.close()

