import requests
import csv



def fetchTableInfo(tableID):
    """Downloads information about a particular table"""
    url = "http://api.censusreporter.org/1.0/table/%s" % (tableID)
    req = requests.get(url)
    if not req.ok:
        print "error in request"
    data = req.json()

    column_list = []
    for key,value in data["columns"].iteritems():
    	title = data["table_title"]
    	denom = data["denominator_column_id"]
    	column_list.append((key, value["column_title"], title, tableID, denom))

    return column_list

# print fetchTableInfo("B19001")

def downloadTableData(tableID, state_name):
	"""Downloads table data by state"""
	states = {"Mississippi": 28, "Oklahoma": 40, "Delaware": 10, "Minnesota": 27, "Illinois": 17, "Arkansas": "05", 
	"New Mexico": 35, "Indiana": 18, "Maryland": 24, "Louisiana": 22, "Idaho": 16, "Wyoming": 56, 
	"Tennessee": 47, "Arizona": "04", "Iowa": 19, "Michigan": 26, "Kansas": 20, "Utah": 49, 
	"Virginia": 51, "Oregon": 41, "Connecticut": "09",  "Montana": 30, "California": "06", "Massachusetts": 25, 
	"West Virginia": 54, "South Carolina": 45, "New Hampshire": 33, "Wisconsin": 55, "Vermont": 50, 
	"Georgia": 13, "North Dakota": 38, "Pennsylvania": 42, "Florida": 12, "Alaska": "02", "Kentucky": 21, 
	"Hawaii": 15, "Nebraska": 31, "Missouri": 29, "Ohio": 39, "Alabama": "01", "New York": 36, "South Dakota": 46, 
	"Colorado": "08", "New Jersey": 34, "Washington": 53, "North Carolina": 37, "District of Columbia": 11, 
	"Texas": 48, "Nevada": 32, "Maine": 23, "Rhode Island": 44}
	stateid = states[state_name]
	state_data_URL = "http://api.censusreporter.org/1.0/data/show/latest?table_ids=%s&geo_ids=140|04000US%s" % (tableID, stateid)
	state_data_req = requests.get(state_data_URL)


	if not state_data_req.ok:
		print "error in request"
	state_data = state_data_req.json()

	big = []
	for geo in state_data['data']:
		mydict= {}
		mydict["geoID"] = geo
		mydict["Fips"] = stateid
		mydict.update(state_data['data'][geo][tableID]['estimate'])

		table_info = (mydict["geoID"], mydict["Fips"])

		for columnID in sorted(state_data['tables'][tableID]['columns'].keys()):
			table_info+= (mydict[columnID],)	
		big.append(table_info)

	return big

# print downloadTableData("B19001", "Maine")
