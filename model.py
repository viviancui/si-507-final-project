import sqlite3
import json

DBNAME = 'whatdidtheysay.db'

def releaseYear(band):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = "SELECT Release_date, count(*) FROM Albums JOIN Artists ON Albums.Artist_id = Artists.Artist_id WHERE Artists.Artist_name='{}' GROUP BY Release_date ORDER BY Release_date".format(band)
    cur.execute(statement)
    x = []
    y = []
    for ele in cur:
        x.append(ele[0])
        y.append(ele[1])
    cur.fetchall()
    return x, y

def trackLength(band):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = "SELECT Albums.Release_date, AVG(Track_length) FROM Tracks JOIN Albums ON Tracks.Album_id=Albums.Album_id JOIN Artists ON Tracks.Artist_id=Artists.Artist_id WHERE Artists.Artist_name='{}' GROUP BY Albums.Release_date ORDER BY Albums.Release_date".format(band)
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    cur.execute(statement)
    x = []
    y = []
    for ele in cur:
        x.append(ele[0])
        y.append(ele[1])
    cur.fetchall()
    return x, y

# FNAME = "bubblechart.json"
def word_count(band):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = "SELECT Word, count(*) FROM Lyrics JOIN Artists ON Lyrics.Artist_id=Artists.Artist_id WHERE Artists.Artist_name='{}' GROUP BY Word ORDER BY count(*) DESC LIMIT 30".format(band)
    cur.execute(statement)
    word_list = []
    count_list = []
    for ele in cur:
        word_list.append(ele[0])
        count_list.append(ele[1])
    cur.fetchall()
    return word_list, count_list

    # third_dict = {}
    # third_dict['name'] = 'draw'
    # third_dict['children'] = []
    # for ele in cur:
    #     data = {}
    #     data['name'] = ele[0]
    #     data['size'] = ele[1]
    #     third_dict['children'].append(data)
    #
    # second_dict = {}
    # second_dict['name'] = 'band'
    # second_dict['children'] = []
    # second_dict['children'].append(third_dict)
    #
    # dataJson = {}
    # dataJson['name'] = 'wordcloud'
    # dataJson['children'] = []
    # dataJson['children'].append(second_dict)
    #
    # cur.fetchall()
    # f = open(FNAME, 'w')
    # content = json.dumps(dataJson)
    # f.write(content)
    # f.close()

# wordJson('Megadeth')

band_list_record = []
#
# def get_band_list():
#     global band_list
#     return band_list

def get_band_name():
    global band_list_record
    print(band_list_record)
    return band_list_record[0]

def add_band_name(bandname):
    global band_list_record
    band_list_record.insert(0, bandname)
    # band["name"] = bandname

spotify_token = {}

def get_token():
    global spotify_token
    return spotify_token['key']

def add_token(token):
    global spotify_token
    spotify_token["key"] = token
