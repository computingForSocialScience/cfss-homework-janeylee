from flask import Flask, render_template, request, redirect, url_for
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
import requests

dbname="playlists"
host="localhost"
user="root"
passwd=""
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')
c = db.cursor()
app = Flask(__name__)




def createNewPlaylist(artist):
    
    create_playlist = """CREATE TABLE IF NOT EXISTS playlists ( 
             id INTEGER PRIMARY KEY AUTO_INCREMENT, 
            rootArtist VARCHAR(255)) 
           ENGINE=MyISAM DEFAULT CHARSET=utf8"""

    create_songs = """CREATE TABLE IF NOT EXISTS songs (
            playlistId VARCHAR (3),
            songOrder VARCHAR (3), 
          artistName VARCHAR (128),
             albumName VARCHAR (128), 
             trackName VARCHAR (128)
             ) ENGINE = MyISAM DEFAULT CHARSET=utf8"""
    c.execute(create_playlist)
    c.execute(create_songs)

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
            

    sql_playlist = """INSERT INTO playlists (rootArtist) VALUES ("%s")""" % (artist)
    c.execute(sql_playlist)
    tracklist = []
    order = 1
    number = c.lastrowid
    for album in random_albums:
        url2 = "https://api.spotify.com/v1/albums/%s/tracks" % (album)
        req2 = requests.get(url2)
        if not req2.ok:
            print "error in request"
        data2 = req2.json()
        playlistId = number
        songOrder = order
        random_track = random.choice(data2['items'])
        name_artist = fetchArtistInfo(fetchAlbumInfo(album)['artist_id'])['name']
        name_album = fetchAlbumInfo(album)['name']
        tracklist.append((playlistId, songOrder, name_artist, name_album, random_track['name']))
        order +=1
    
    insertQuery = '''INSERT INTO songs (playlistId, songOrder, artistName, albumName, trackName) VALUES (%s, %s, %s, %s, %s)'''
    c.executemany(insertQuery, tracklist)


    db.commit()
    c.close()
    db.close()

@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return render_template('index.html')


@app.route('/playlists/')
def make_playlists_resp():
    sql = """SELECT * from playlists"""
    c.execute(sql)
    playlists={}
    for tup in c.fetchall():
        (iden, play) = tup
        playlists[iden] = play
    return render_template('playlists.html',playlists=playlists)


@app.route('/playlist/<playlistId>')
def make_playlist_resp(playlistId):
    sql2 = """SELECT songOrder, artistName, albumName, trackName from songs where playlistId = '%s'""" % (playlistId)
    c.execute(sql2)
    songs=[]
    for n in c.fetchall():
        print n
        songs.append(n)
    return render_template('playlist.html',songs=songs)


@app.route('/addPlaylist/',methods=['GET','POST'])
def add_playlist():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return render_template('addPlaylist.html') 
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        artistName = request.form['artistName']
        createNewPlaylist("%s") % (artistName)
        return redirect("/playlists/")



# problems:  json error, should tables really be recreated each time 
if __name__ == '__main__':
    app.debug=True
    app.run()