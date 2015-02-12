import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import plotBarChart

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print "input artists are ", artist_names
    list_of_artist_ids = []

    for artist in artist_names:
    	artist_id = fetchArtistId(artist)
    	list_of_artist_ids.append(artist_id)
    	

	list_of_artist_dicts = []

	for artist_id in list_of_artist_ids:
		artist_info = fetchArtistInfo(artist_id)
		list_of_artist_dicts.append(artist_info)

	writeArtistsTable(list_of_artist_dicts)	

	list_of_album_ids = []
	for artist in list_of_artist_ids:
		list_of_album_ids += fetchAlbumIds(artist)

	list_of_album_dicts = []
	for album in list_of_album_ids:
		list_of_album_dicts.append(fetchAlbumInfo(album))

	writeAlbumsTable(list_of_album_dicts)

	plotBarChart()
    

