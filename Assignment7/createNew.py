# from flask import Flask, render_template, request, redirect, url_for
import pymysql
import sys
from artistNetworks import *
from analyzeNetworks import *
from fetchArtist import *
from fetchAlbums import *
import random
from io import open
import unicodecsv
import datetime

dbname="playlists"
host="localhost"
user="root"
passwd=""
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')
c = db.cursor()
# app = Flask(__name__)

def createNewPlaylist(artist):
    artist_id = fetchArtistId(artist)
    m = writeEdgeList(artist_id, 2, "%s.csv" % (artist_id))
    combined = readEdgeList(m)
    artist_network = pandasToNetworkX(combined)
    list_of_artists = []
    x = 30 # pick 30 random 
    while x > 0:
        rand = randomCentralNode(artist_network)
        list_of_artists.append(rand)
        x -= 1
    random_albums = [] #1 random album per artist

    for art in list_of_artists: # 30 artists

        url = "https://api.spotify.com/v1/artists/%s/albums" % (art)
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
        playlist.write(u'"%s","%s","%s"\n' % (name_artist, name_album, random_track['name']))
    playlist.close()


    sql_playlist = """INSERT INTO playlists (rootArtist) VALUES ('%s')""" % (artist)
    print sql_playlist

    iden = """SELECT id FROM playlists WHERE rootArtist = '%s'""" % (artist)
    print iden
    c.execute(sql_playlist)
    print c.execute(iden)

    f = open("playlist.csv", encoding='utf_8')
    csv_file = unicodecsv.reader(f, encoding='utf-8')

    header = True
    order = 1
    for l in csv_file:
    
        if header:
            header = False
            continue
        playlistId = c.execute(iden)
        songOrder = order
        artistName = l[0]
        albumName = l[1]
        trackName = l[2]
        order += 1

        sql_songs = """INSERT INTO songs (playlistId, songOrder, artistName, albumName, trackName) 
        VALUES ('%s', '%s', "%s", "%s", "%s")""" % (playlistId, songOrder, artistName, albumName, trackName)

        # print sql_songs
        c.execute(sql_songs)



    db.commit()
    c.close()
    db.close()

createNewPlaylist("Mika")