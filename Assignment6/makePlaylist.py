
import sys
from artistNetworks import *
from analyzeNetworks import *
from fetchArtist import *
from fetchAlbums import *
import random
from io import open


artist_names = sys.argv[1:]
list_of_artist_ids = []

for artist in artist_names:
	artist_id = fetchArtistId(artist)
	list_of_artist_ids.append(artist_id)

list_of_csvs = []
for artist_id in list_of_artist_ids:
	m = writeEdgeList(artist_id, len(artist_names), "%s.csv" % (artist_id))
	list_of_csvs.append(m)

combined = []
num_artists = len(list_of_csvs)
print num_artists
# if len(list_of_csvs) == 1:
# 	combined = readEdgeList(list_of_csvs[0])
# elif len(list_of_csvs) > 1: 
	# for x in range(len(list_of_csvs)):
	# 	part = combineEdgeLists(combined, readEdgeList(list_of_csvs[x]))
	# 	combined += part
if num_artists == 1:
	combined = readEdgeList(list_of_csvs[0])
elif num_artists == 2:
	combined = combineEdgeLists(readEdgeList(list_of_csvs[0]), readEdgeList(list_of_csvs[1]))
else:
	pass


artist_network = pandasToNetworkX(combined)

list_of_artists = []
x = 30
while x > 0:
	rand = randomCentralNode(artist_network)
	list_of_artists.append(rand)
	x -= 1
# print list_of_artists


random_albums = [] #1 random album per artist

for artist in list_of_artists: # 30 artists
	url = "https://api.spotify.com/v1/artists/%s/albums" % (artist)
	req = requests.get(url)
	if not req.ok:
		print "error in request"
	data = req.json()
	list_of_albums = [] # any number of albums
	for album in range(len(data['items'])):
		album_id = data['items'][album]['id']
		list_of_albums.append(album_id)

	random_album = random.choice(list_of_albums)

	random_albums.append(random_album)
		
playlist = open("playlist.csv", "w", encoding='utf-8') # , encoding='utf-8' ??
playlist.write(u'artist_name, album_name, track_name\n')


for album in random_albums:
	url2 = "https://api.spotify.com/v1/albums/%s/tracks" % (album)
	req2 = requests.get(url2)
	if not req2.ok:
		print "error in request"
	data2 = req2.json()

	random_track = random.choice(data2['items'])
	name_artist = fetchArtistInfo(fetchAlbumInfo(album)['artist_id'])['name']
	name_album = fetchAlbumInfo(album)['name']

	playlist.write('"%s","%s","%s"\n' % (name_artist, name_album, random_track['name']))
playlist.close



	