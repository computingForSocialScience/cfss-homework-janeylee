import pandas as pd
import networkx as nx
import numpy

def readEdgeList(filename):
	df = pd.read_csv(filename)
	if len(df.columns) > 2:
		print "This has more than 2 columns. Printing only the first two..."
	return df
	# how to print only first two columns?

def degree(edgeList, in_or_out):
	if in_or_out == "out":
		df = pd.DataFrame(edgeList['artist1'].value_counts())
		return df
	if in_or_out == "in":	
		df = pd.DataFrame(edgeList['artist2'].value_counts())
		return df

# print degree(readEdgeList("testEdgeList.csv"),'out')[0]


def combineEdgeLists(edgeList1,edgeList2):
	concatenated = pd.concat([edgeList1,edgeList2])
	return concatenated.drop_duplicates()

def pandasToNetworkX(edgeList):

	g = nx.DiGraph()
	for artist1,artist2 in edgeList.to_records(index=False):
		g.add_edge(artist1,artist2)
	return g

def randomCentralNode(inputDiGraph):
	eigen = nx.eigenvector_centrality(inputDiGraph)
	# calculated by assessing how well connected an individual is to the parts 
	# of the network with the greatest connectivity 
	# returns a dictionary
	total = sum(eigen.values())
	factor = 1/total
	nc_dict = eigen
	nc_dict = {key:value*factor for key,value in nc_dict.iteritems()}
	random = numpy.random.choice(nc_dict.keys(), p=nc_dict.values())
	return random

