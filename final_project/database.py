from collectData import *
import pymysql


list_of_tables = ['B19001', 'B27001']

dbname="acs_survey"
host="localhost"
user="root"
passwd=""
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

c = db.cursor()
create_columninfo = """CREATE TABLE IF NOT EXISTS column_info ( 
         ACScolumnId VARCHAR (128),
         columnName VARCHAR (128),
         ACStableId VARCHAR (255),
         tableName VARCHAR (128),
         denom VARCHAR (128)
         )
       ENGINE=MyISAM DEFAULT CHARSET=utf8"""
c.execute(create_columninfo)


# create_ACSinfo = """CREATE TABLE IF NOT EXISTS ACSdata (
	# index INTEGER PRIMARY KEY AUTO_INCREMENT, 
	# geoID VARCHAR (128), 
	# FIPS VARCHAR (3),
#          ) ENGINE = MyISAM DEFAULT CHARSET=utf8"""
#  It will have as many columns as the corresponding ACS table has
# HOW DO I KNOW HOW TO MAKE THE TABLE THEN???
# why do we need index on geo id column and fips code column? how do tht?
# c.execute(create_songs)

insertQuery = '''INSERT INTO column_info (ACScolumnId, columnName, ACStableId, tableName, denom) VALUES (%s, %s, %s, %s, %s)'''

for table in list_of_tables:
	c.executemany(insertQuery, fetchTableInfo(table))
c.close()
