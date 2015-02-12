import requests
from datetime import datetime

def fetchAlbumIds(artist_id):
    url = "https://api.spotify.com/v1/artists/"+ artist_id + "/albums?market=US&album_type=album&limit=50"
    req = requests.get(url)
    if not req.ok:
        print "error in request"
    data = req.json()
    list_of_album_ids = []
    for album in data['items']:
    	list_of_album_ids.append(album['id'])
    return list_of_album_ids

# print fetchAlbumIds('4QQgXkCYTt3BlENzhyNETg')

def fetchAlbumInfo(album_id):
    """Using the Spotify API, take an album ID 
    and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
    """
    url2 = "https://api.spotify.com/v1/albums/" + album_id
    req2 = requests.get(url2)
    if not req2.ok:
    	print "error in request"
    data2 = req2.json()
    album_dict = {}
    album_dict['artist_id'] = data2['artists'][0]['id']
    album_dict['album_id'] = album_id
    album_dict['name'] = data2['name']
    album_dict['year'] = data2['release_date'][0:4]
    album_dict['popularity'] = data2['popularity']
    return album_dict

