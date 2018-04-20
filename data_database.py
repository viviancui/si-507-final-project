import sqlite3
import csv
import json
import musixmatch_request
import frequency

DBNAME = 'whatdidtheysay.db'

def create_db():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    statement = '''
        DROP TABLE IF EXISTS 'Lyrics';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Tracks';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Albums';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Artists';
    '''
    cur.execute(statement)

    statement = '''
            CREATE TABLE 'Artists' (
                'Artist_id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Artist_spotify_id' TEXT NOT NULL,
                'Artist_name' TEXT NOT NULL
            );
        '''
    cur.execute(statement)
    conn.commit()

    statement = '''
            CREATE TABLE 'Albums' (
                'Album_id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Album_spotify_id' TEXT NOT NULL,
                'Album_name' TEXT NOT NULL,
                'Release_date' TEXT,
                'Artist_id' INTEGER NOT NULL
            );
        '''
    cur.execute(statement)
    conn.commit()

    statement = '''
            CREATE TABLE 'Tracks' (
                'Track_id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Track_spotify_id' TEXT NOT NULL,
                'Track_name' TEXT NOT NULL,
                'Track_length' INTEGER,
                'Album_id' INTEGER NOT NULL,
                'Artist_id' INTEGER NOT NULL
            );
        '''
    cur.execute(statement)
    conn.commit()

    statement = '''
            CREATE TABLE 'Lyrics' (
                'Lyrics_word_Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Word' TEXT NOT NULL,
                'Track_id' INTEGER NOT NULL,
                'Album_id' INTEGER NOT NULL,
                'Artist_id' INTEGER NOT NULL
            );
        '''
    cur.execute(statement)
    conn.commit()

# create_db()

def populate_Artists(artist):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    Artist_spotify_id = artist.artist_id
    Artist_name = artist.artist_name
    insertion = (None, Artist_spotify_id, Artist_name)
    statement = 'INSERT INTO "Artists" '
    statement += 'VALUES (?, ?, ?)'
    cur.execute(statement, insertion)
    conn.commit()



def populate_Albums(album, artist_id):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    Album_spotify_id = album.album_id
    Album_name = album.album_name
    Release_date = album.album_release_date[:4]
    insertion = (None, Album_spotify_id, Album_name, Release_date, artist_id)
    statement = 'INSERT INTO "Albums" '
    statement += 'VALUES (?, ?, ?, ?, ?)'
    cur.execute(statement, insertion)
    conn.commit()



def find_artist_id(spotify_artist_id):
    conn = sqlite3.connect(DBNAME)
    cur2 = conn.cursor()
    cur2 = cur2.execute('SELECT Artist_id FROM Artists WHERE Artist_spotify_id = ' + str(spotify_artist_id))
    Artist_id = cur2.fetchone()[0]
    return Artist_id



def populate_Tracks(track, album_id, artist_id):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    Track_spotify_id = track.track_id
    Track_name =  track.track_name
    Track_length = track.track_length
    insertion = (None, Track_spotify_id, Track_name, Track_length, album_id, artist_id)
    statement = 'INSERT INTO "Tracks" '
    statement += 'VALUES (?, ?, ?, ?, ?, ?)'
    cur.execute(statement, insertion)
    conn.commit()

def find_album_id(spotify_album_id):
    conn = sqlite3.connect(DBNAME)
    cur2 = conn.cursor()
    cur2 = cur2.execute('SELECT Album_id FROM Albums WHERE Album_spotify_id = ' + str(spotify_album_id))
    album_id = cur2.fetchone()[0]
    return album_id

def get_band_list():
    conn = sqlite3.connect(DBNAME)
    cur4 = conn.cursor()
    cur4 = cur4.execute('SELECT Artist_name FROM Artists')
    artist_list = []
    for ele in cur4:
        artist_list.append(ele[0])
    print(artist_list)
    return artist_list

# FREQUENCYJSON = 'frequency_result_archenemy.json'
def populate_Lyrics(word, track_id, album_id, artist_id):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    insertion = (None, word, track_id, album_id, artist_id)
    statement = 'INSERT INTO "Lyrics" '
    statement += 'VALUES (?, ?, ?, ?, ?)'
    cur.execute(statement, insertion)
    conn.commit()

def find_track_id(spotify_track_id):
    conn = sqlite3.connect(DBNAME)
    cur2 = conn.cursor()
    cur2 = cur2.execute('SELECT Track_id FROM Tracks WHERE Track_spotify_id = ' + str(spotify_track_id))
    track_id = cur2.fetchone()[0]
    return track_id

# band = input("Please put in the name of the band/artist: ")

def populate_Database(band):
    artist_obj = musixmatch_request.get_artist_obj(band)
    populate_Artists(artist_obj)

    spotify_artist_id = artist_obj.artist_id
    musix_album_json = musixmatch_request.get_album(spotify_artist_id)
    musix_album_list = musix_album_json["message"]["body"]["album_list"]
    album_obj_list = musixmatch_request.get_album_obj(musix_album_list)

    artist_id = find_artist_id(spotify_artist_id)
    album_id_list = []
    for ele in album_obj_list:
        populate_Albums(ele, artist_id)
        album_id_list.append(ele.album_id)

    for ele in album_obj_list:
        album_id = find_album_id(ele.album_id)
        musix_track_json = musixmatch_request.get_tracks(ele.album_id)["message"]["body"]["track_list"]
        track_obj_list = musixmatch_request.get_track_obj_list(musix_track_json)
        for ele in track_obj_list:
            populate_Tracks(ele, album_id, artist_id)
            spotify_track_id = ele.track_id
            track_id = find_track_id(spotify_track_id)
            lyrics_raw = musixmatch_request.get_lyrics(spotify_track_id)
            lyrics_str = musixmatch_request.prettify_lyrics(lyrics_raw)
            lyrics = frequency.clear_lyrics(lyrics_str)
            total_word_list = frequency.tokenize(lyrics)
            # print(total_word_list)
            for ele in total_word_list:
                word = frequency.refine_word(ele)
                if word != 999:
                    populate_Lyrics(word, track_id, album_id, artist_id)
