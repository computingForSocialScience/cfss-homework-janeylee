import unicodecsv as csv
import matplotlib.pyplot as plt

def getBarChartData():
    f_artists = open('artists.csv')
    # Open the artists.csv file
    f_albums = open('albums.csv')
    # Open albums.csv file

    artists_rows = csv.reader(f_artists)
    # gets all the artist rows from the csv files
    albums_rows = csv.reader(f_albums)
    # gets all the album rows from csv files

    artists_header = artists_rows.next()
    # grabs the first row of artist_rows which is the header
    albums_header = albums_rows.next()
    # grabs the first row of artist_rows which is the header

    artist_names = []
    
    decades = range(1900,2020, 10)
    decade_dict = {}
    for decade in decades:
        decade_dict[decade] = 0
    # creates a dictionary with decades from 1900 to 2020 as keys and value as 0
    
    for artist_row in artists_rows:
        if not artist_row:
            continue # if there is no artist_row, finish the loop
        artist_id,name,followers, popularity = artist_row
        artist_names.append(name)
        # for each artist, append his/her name to artist_names

    for album_row  in albums_rows:
        if not album_row:
            continue # if there is no album_row, finish the loop
        artist_id, album_id, album_name, year, popularity = album_row
        for decade in decades:
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)):
                decade_dict[decade] += 1
                break
        # for each year decade-ending or -beginning year, 
        # check if the album's year is between that year and 
        # the start of the next decade. If it is, increase the count
        # for that decade by 1, then exit the loop (since the if statement won't
        # hold for any more years)

    x_values = decades
    # X axis is the decades
    y_values = [decade_dict[d] for d in decades]
    # Y axis is the count of albums in each decade from my album list
    return x_values, y_values, artist_names

def plotBarChart():
    x_vals, y_vals, artist_names = getBarChartData()
    
    fig , ax = plt.subplots(1,1)
    ax.bar(x_vals, y_vals, width=10)
    ax.set_xlabel('decades')
    ax.set_ylabel('number of albums')
    ax.set_title('Totals for ' + ', '.join(artist_names))
    plt.show()
    # Create the bar chart showing the number of albums for each decade


    
