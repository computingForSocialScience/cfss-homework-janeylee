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

dbname="playlists"
host="localhost"
user="root"
passwd=""
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')
c = db.cursor()
app = Flask(__name__)

# CREATE TABLE playlists ( 
#              id INTEGER PRIMARY KEY AUTO_INCREMENT, 
#             rootArtist VARCHAR(255)) 
#            ENGINE=MyISAM DEFAULT CHARSET=utf8;

#            CREATE TABLE songs (
#             playlistId VARCHAR (3),
#             songOrder VARCHAR (3), 
#           artistName VARCHAR (128),
#              albumName VARCHAR (128), 
#              trackName VARCHAR (128)
#              ) ENGINE = MyISAM DEFAULT CHARSET=utf8;

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
    print list_of_artists

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

        print sql_songs
        c.execute(sql_songs)



    db.commit()
    c.close()
    db.close()

# createNewPlaylist("Patti Smith")


# @app.route('/')
# def make_index_resp():
#     # this function just renders templates/index.html when
#     # someone goes to http://127.0.0.1:5000/
#     return render_template('index.html')


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
        return(render_template('addPlaylist.html'))
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        artistName = request.form.get('artistName')
        createNewPlaylist('%s') % (artistName)
        return(redirect("/playlists/"))



# problems: encoding, json error, c.execute(iden) doesn't 
# get the right playlist id so it adds to already existing playlist 
if __name__ == '__main__':
    app.debug=True
    app.run()