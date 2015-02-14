import requests
import pandas as pd

def getRelatedArtists(artistID):
	url = "https://api.spotify.com/v1/artists/%s/related-artists" % (artistID)
	req = requests.get(url)
	if not req.ok:
		print "error in request"
	data = req.json()  	
	list_of_artists = []
	for artist in range(len(data['artists'])):
		artist_id = data['artists'][artist]['id']
		list_of_artists.append(artist_id)
	return list_of_artists

# getRelatedArtists("2mAFHYBasVVtMekMUkRO9g")

def getDepthEdges(artistID, depth):
	related_artists = getRelatedArtists(artistID) #gives a list of artists
	tuples = []

	for artist in related_artists:
		dyad = (artistID, artist)
		tuples.append(dyad)

	if depth == 1:
		return tuples
	
	new = []
	if depth > 1:
		while depth > 1: 
			for each in tuples: # [('A','B'), ('A','C')]
				more_artists = getRelatedArtists(each[1]) #[D, E]
				new += [(each[1],x) for x in more_artists]
			depth = depth - 1
		tuples += new
		return tuples

# print getDepthEdges('2mAFHYBasVVtMekMUkRO9g', )


def getEdgeList(artistID, depth):
	data = getDepthEdges(artistID, depth)
	df = pd.DataFrame(data)
	return df

print getEdgeList('2mAFHYBasVVtMekMUkRO9g',2)[0:10]

def writeEdgeList(artistID,depth,filename):
	doc = getEdgeList(artistID, depth)
	doc.to_csv(filename, index=False, header=False)

# writeEdgeList('2mAFHYBasVVtMekMUkRO9g',2,'Edges.csv')

