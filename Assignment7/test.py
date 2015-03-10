from io import open
import unicodecsv

f = open("playlist.csv")
csv_file = unicodecsv.reader(f)

# entering the playlist info from csv to MySQL. how to enter playlist id and songorder?
header = True

order = 1

for l in csv_file:

    if header:
        header = False
        continue
    # playlistId = iden
    songOrder = order
    artistName = l[0]
    albumName = l[1]
    trackName = l[2]
    order +=1
    # print songOrder, artistName, albumName, trackName


    sql_songs = """INSERT INTO songs (songOrder, artistName, albumName, trackName) VALUES ('%s', '%s', '%s', '%s')""" % (songOrder, artistName, albumName, trackName)
    print sql_songs