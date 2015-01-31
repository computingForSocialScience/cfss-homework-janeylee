from __future__ import division
import matplotlib.pyplot as plt
import csv
import sys
import re

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)


HPpermits = readCSV("permits_hydepark.csv")

def get_avg_latlng(neighborhood):
	'''Computes the average latitude and longitude of construction permits
	 in Hyde Park and prints it to the console.'''
	lat = 0
	longi = 0
	for permit in range(len(neighborhood)):
		if neighborhood[permit][-2]: # one entry missing a lat and long
			lat += float(neighborhood[permit][-2])
			longi += float(neighborhood[permit][-3])
	avglat = lat/len(neighborhood)
	avglongi = longi/len(neighborhood)

	return "average latitude = " + str(avglat) + " average longitude = " + str(avglongi)



def zip_code_barchart(neighborhood):
	'''Creates .jpg bar chart of contractor zip codes for permits in Hyde Park.'''
	counts = {}
	for permit in range(len(neighborhood)):
		for number in range(28, 130, 7): 
		#contractor zip codes start at column 29 (=index 28) and end at column 127 (=index 128). 
		#zip codes occur every 7th index
			if re.match('\d{5}', neighborhood[permit][number]): #make sure it's a valid zip code
				if int(neighborhood[permit][number][0:5]) in counts:
					counts[int(neighborhood[permit][number][0:5])] += 1
				else:
					counts[int(neighborhood[permit][number][0:5])] = 1
	zips = range(len(counts.keys()))
	plt.figure(figsize=(20,8))
	plt.bar(zips, counts.values(), align='center')
	plt.xticks(zips, counts.keys(), rotation=90)
	plt.xlabel("Zip codes")
	plt.ylabel("Frequency")
	plt.title("Bar Chart of Contractor Zip Codes for Permits in Hyde Park")
	plt.savefig('barchart.jpg')

	plt.show()

if sys.argv[1] == 'latlong':
	print get_avg_latlng(HPpermits)
if sys.argv[1] == 'hist':
	zip_code_barchart(HPpermits)
