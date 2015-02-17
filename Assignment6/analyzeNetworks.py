import pandas as pd
import networkx as nx

def readEdgeList(filename):
	df = pd.read_csv(filename)
	if len(df.columns) > 2:
		print "This has more than 2 columns. Printing only the first two..."
	return df
	# how to print only first two columns?

artist_edge_list = readEdgeList("Edges.csv")


def degree(edgeList, in_or_out):
	if in_or_out == "out":
		df = pd.DataFrame(edgeList['artist1'].value_counts())
		return df
	if in_or_out == "in":	
		df = pd.DataFrame(edgeList['artist2'].value_counts())
		return df

out_list = degree(artist_edge_list, "out")
in_list = degree(artist_edge_list, "in")

def combineEdgeLists(edgeList1,edgeList2):
	concatenated = pd.concat([edgeList1,edgeList2])
	return concatenated.drop_duplicates()

def pandasToNetworkX(edgeList):

	g = nx.DiGraph()
	for artist1,artist2 in edgeList.to_records(index=False):
		g.add_edge(artist1,artist2)

pandasToNetworkX(network)




