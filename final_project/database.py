from collectData import *
import pymysql
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)



list_of_tables = ['B19001', 'B27001', 'B27010', 'B21004', 'B21001']

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
# # ?????????????????????????
#          ) ENGINE = MyISAM DEFAULT CHARSET=utf8"""
#  It will have as many columns as the corresponding ACS table has
# HOW DO I KNOW HOW TO MAKE THE TABLE THEN???
# why do we need index on geo id column and fips code column? how do tht?
# c.execute(create_songs)

insertQuery = '''INSERT INTO column_info (ACScolumnId, columnName, ACStableId, tableName, denom) VALUES (%s, %s, %s, %s, %s)'''

for table in list_of_tables:
	c.executemany(insertQuery, fetchTableInfo(table))
c.close()

@app.route('/', methods=["GET", "POST"])
def index():
	fips_URL = "http://cfss.uchicago.edu/data/FIPS.json"
	fips_req = requests.get(fips_URL)
	if not fips_req.ok:
		print "error in request"
	fips_dict = fips_req.json()
	states = fips_dict.keys()

	if request.method == 'GET':
		return render_template('index.html', states = states)
	if request.method == 'POST':
  		pass
  		
@app.route('/compare?state=<FIPSCode>&col1=<columnId1>&col2=<columnId2>')
def compare():
	pass

if __name__ == '__main__':
    app.debug=True
    app.run()