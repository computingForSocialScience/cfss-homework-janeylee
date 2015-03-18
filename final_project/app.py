from collectData import *
import pymysql
from flask import Flask, render_template, request, redirect, url_for

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components
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
	c.execute(join)
	print "executed join" # it takes about 40 minutes for this to print after executing 'join'
	# y = 
	# x = 
	# how do you access one column from join to assign it to x and y?

	p = figure(title='Household Income versus Commute Time',plot_width=500,plot_height=400)
	p.line(x,y)
	p.xaxis.axis_label = "Household Income"
	p.yaxis.axis_label = "Commute Time"
	figJS,figDiv = components(p,CDN)


	return render_template('chart.html',column1=column1,column2=column1, state = state, y=y, figJS=figJS,figDiv=figDiv)

	c.close()

if __name__ == '__main__':
    app.debug=True
    app.run()
