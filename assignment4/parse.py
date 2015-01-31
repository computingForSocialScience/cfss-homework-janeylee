from __future__ import division

import csv
import sys

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
	lat = 0
	longi = 0
	for permit in range(len(neighborhood)):
		lat += float(neighborhood[permit][-2])
		longi += float(neighborhood[permit][-3])
	avglat = lat/len(neighborhood)
	avglongi = longi/len(neighborhood)

	return "average latitude = " + str(avglat) + " average longitude = " + str(avglongi)
print get_avg_latlng(HPpermits)

