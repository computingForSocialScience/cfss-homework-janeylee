from io import open
import fetchArtist
import fetchAlbums

# list_of_artists = [fetchArtist.fetchArtistInfo("0TcYeHEK9sBtv7xPbKhzHz"), fetchArtist.fetchArtistInfo("0vYkHhJ48Bs3jWcvZXvOrP")]

def writeArtistsTable(artist_info_list):
    """Given a list of dictionaries, each as returned from 
    fetchArtistInfo(), write a csv file 'artists.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY
    """
    f = open('artists.csv', 'w', encoding='utf-8')
    f.write(u'ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY\n')
    for artist in artist_info_list:
        f.write('%s,"%s",%d,%d\n' % (artist['id'], artist['name'], artist['followers'], artist['popularity']))
    f.close()

# writeArtistsTable(list_of_artists)

# list_of_albums = [fetchAlbums.fetchAlbumInfo("67epO9J9KoY8KSFA4xC4kA"), fetchAlbums.fetchAlbumInfo("00tuL4qPxBs3w8S1BaG3Zv")]
      
def writeAlbumsTable(album_info_list):
    """
    Given list of dictionaries, each as returned
    from the function fetchAlbumInfo(), write a csv file
    'albums.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY
    """
    g = open('albums.csv', 'w', encoding='utf-8')
    g.write(u'ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY\n')
    for album in album_info_list:
        g.write('%s,%s,"%s",%s,%d\n' % (album["album_id"],album["artist_id"],album["name"],int(album["year"]),int(album['popularity'])))
    g.close()

# writeAlbumsTable(list_of_albums)