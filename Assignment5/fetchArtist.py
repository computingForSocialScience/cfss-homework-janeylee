import sys
import requests
import csv



def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    url = "https://api.spotify.com/v1/search?q=" + name + "&type=artist"
    req = requests.get(url)
    if not req.ok:
        print "error in request"
    data = req.json()

    return data['artists']['items'][0]['id']


# fetchArtistId("Chumbawamba")
# fetchArtistId("Patti Smith")


def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
`   returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
    url2 = "https://api.spotify.com/v1/artists/" + artist_id

    req2 = requests.get(url2)
    if not req2.ok:
        print "error in request"
    data2 = req2.json()
    artist_dict = {}

    artist_dict['followers'] = data2['followers']['total']
    artist_dict['genres'] = data2['genres']
    artist_dict['id'] = data2['id']
    artist_dict['name'] = data2['name']
    artist_dict['popularity'] = data2['popularity']
    return artist_dict
# print fetchArtistInfo('57anmI1X2hXWPrNagFdzZr')


