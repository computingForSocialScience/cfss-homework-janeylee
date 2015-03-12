import requests
import csv

'''
B27001	Health Insurance Coverage Status by Sex by Age
Table B19001: Household Income
B27010	Types of Health Insurance Coverage by Age
Table B21004: Median Income by Veteran Status by Sex for the Civilian Population 18 Years and Over With Income
Table B21001: Sex by Age by Veteran Status for the Civilian Population 18 Years and Over

'''


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
	fips_URL = "http://cfss.uchicago.edu/data/FIPS.json"
	fips_req = requests.get(fips_URL)
	if not fips_req.ok:
		print "error in request"
	fips_dict = fips_req.json()
	stateid = fips_dict[state_name]

	state_data_URL = "http://api.censusreporter.org/1.0/data/show/latest?table_ids=%s&geo_ids=140|04000US%s" % (tableID, stateid)
	state_data_req = requests.get(state_data_URL)

	if not state_data_req.ok:
		print "error in request"
	state_data = state_data_req.json()

	big = []
	for geo in state_data['data']:
		table_info = tuple(state_data['data'][geo]['B19001']['estimate'].values())
		info = (geo, stateid) + table_info
		big.append(info)

	return big

# print downloadTableData("B19001", "Alabama")

# [u'14000US17031062700', '1', 203.0, 44.0, 160.0, 193.0, 0.0, 37.0, 96.0, 20.0, 0.0, 43.0, 40.0, 31.0, 14.0, 75.0, 46.0, 141.0, 1143.0]
# should this also get the column headers.







