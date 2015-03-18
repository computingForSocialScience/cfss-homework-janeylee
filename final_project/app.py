from collectData import *
import pymysql
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


dbname="acs_survey2"
host="localhost"
user="root"
passwd=""
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')


@app.route('/', methods=["GET", "POST"])
def index():
	c = db.cursor()
	fips_URL = "http://cfss.uchicago.edu/data/FIPS.json"
	fips_req = requests.get(fips_URL)
	if not fips_req.ok:
		print "error in request"
	fips_dict = fips_req.json()

	sql2 = """SELECT * from column_info order by ACScolumnId"""
	c.execute(sql2)
	column_titles = []
	for x in c.fetchall():
		column_titles.append(x)


	if request.method == 'GET':
		return render_template('index.html', column_titles = column_titles, fips_dict = fips_dict)
	if request.method == 'POST':
  		pass
  		
@app.route('/compare')
def compare():
	c = db.cursor()
	column1 = request.args['column1']
	column2 = request.args['column2']
	state = request.args['state']
	join = """SELECT commute.%s, income.%s FROM commute, income WHERE commute.geoID=income.geoID"""  % (column1, column2)
	print join
	c.execute(join)
	print "executed join"



	return render_template('chart.html',column1=column1,column2=column1, state = state)

	# ImmutableMultiDict([('state', u'Mississippi'), ('column1', u'B19001003'), ('column2', u'B27001007')])
	# what table are those columns in
	# contrusct query that draws data
	# put bokeh/regression code goes here 
	# send to template 
	c.close()

if __name__ == '__main__':
    app.debug=True
    app.run()
