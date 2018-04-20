import json
import requests
import secrets

apikey = secrets.api_key

CACHE_FNAME = "dataall_cache.json"
try:
    cache_file = open(CACHE_FNAME, "r")
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def unique_i(baseurl, params_dict, mtype):
    alphabetized_keys = params_dict.keys()
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params_dict[k]))
    return baseurl + "&".join(res) + mtype

def get_artist_request(band):
    baseurl = "http://api.musixmatch.com/ws/1.1/"
    params_dict = {}
    mtype = "artist.search?"
    params_dict["q_artist"] = band
    # params_dict["q_artist"] = "Iron Maiden"
    # params_dict["q_artist"] = input("Which band/artist do you like: ")
    params_dict["apikey"] = apikey

    unique_ident = unique_i(baseurl, params_dict, mtype)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        musix_response = requests.get(baseurl + mtype, params_dict)
        musix_text = musix_response.text
        # musix_json = json.loads(musix_text)
        CACHE_DICTION[unique_ident] = json.loads(musix_text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        f = open(CACHE_FNAME, "w")
        f.write(dumped_json_cache)
        f.close()
        return CACHE_DICTION[unique_ident]
        # print(musix_json)

class Artist():
    def __init__(self, artist_dict={}):
        self.artist_name = artist_dict["artist"]["artist_name"]
        self.artist_id = artist_dict["artist"]["artist_id"]
        self.artist_mbid = artist_dict["artist"]["artist_mbid"]
        self.artist_twitter_url = artist_dict["artist"]["artist_twitter_url"]

# print(artist_id)

# band = input("Please put in the name of the band/artist: ")

def get_artist_obj(band):
    musix_json = get_artist_request(band)
    print(musix_json)
    musix_artist_list = musix_json["message"]["body"]["artist_list"]
    artist_id_list = []
    for ele in musix_artist_list:
        artist_id_list.append(Artist(ele))
    # artist_id = artist_id_list[0].artist_id
    artist_obj = artist_id_list[0]
    return artist_obj

# x = get_artist_obj('Megadeth')

# artist_obj = get_artist_id(band)
# print("-"*20)
# print(artist_obj)
# print("-"*20)

def get_album(artist_id):
    baseurl = "http://api.musixmatch.com/ws/1.1/"
    mtype = "artist.albums.get?"
    params_dict = {}
    params_dict["artist_id"] = artist_id
    params_dict["page_size"] = 100
    params_dict["apikey"] = apikey
    unique_ident = unique_i(baseurl, params_dict, mtype)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        musix_response = requests.get(baseurl + mtype, params_dict)
        musix_text = musix_response.text
        # musix_album_json = json.loads(musix_text)
        # print(musix_album_json)
        CACHE_DICTION[unique_ident] = json.loads(musix_text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        f = open(CACHE_FNAME, "w")
        f.write(dumped_json_cache)
        f.close()
        return CACHE_DICTION[unique_ident]

# musix_album_json = get_album(artist_id)
# musix_album_list = musix_album_json["message"]["body"]["album_list"]
# print(musix_album_list)
# print("-"*20)

class Album():
    def __init__(self, album_dict={}):
        self.album_id = album_dict["album"]["album_id"]
        self.album_name = album_dict["album"]["album_name"]
        self.album_release_date = album_dict["album"]["album_release_date"]

def get_album_obj(musix_album_list):
    album_obj_list = []
    for ele in musix_album_list:
        album_obj_list.append(Album(ele))
    return album_obj_list

# album_id_list = []
# album_name_list = []
# album_release_date_list = []
# for ele in musix_album_list:
#     album_id_list.append(Album(ele).album_id)
#     album_name_list.append(Album(ele).album_name)
#     album_release_date_list.append(Album(ele).album_release_date)
# print(album_id_list)
# print("-"*20)
# print(album_name_list)
# print("-"*20)
# print(album_release_date_list)
# print("-"*20)

def get_tracks(album_id):
    baseurl = "http://api.musixmatch.com/ws/1.1/"
    mtype = "album.tracks.get?"
    params_dict = {}
    params_dict["album_id"] = album_id
    params_dict["page_size"] = 100
    params_dict["apikey"] = apikey
    unique_ident = unique_i(baseurl, params_dict, mtype)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        musix_response = requests.get(baseurl + mtype, params_dict)
        musix_text = musix_response.text
        CACHE_DICTION[unique_ident] = json.loads(musix_text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        f = open(CACHE_FNAME, "w")
        f.write(dumped_json_cache)
        f.close()
        return CACHE_DICTION[unique_ident]

class Track():
    def __init__(self, track_dict={}):
        self.track_id = track_dict["track"]["track_id"]
        self.track_name = track_dict["track"]["track_name"]
        self.track_length = track_dict["track"]["track_length"]

def get_track_obj_list(musix_track_json):
    track_obj_list = []
    for ele in musix_track_json:
        track_obj_list.append(Track(ele))
    return track_obj_list

def get_lyrics(track_id):
    baseurl = "http://api.musixmatch.com/ws/1.1/"
    mtype = "track.lyrics.get?"
    params_dict = {}
    params_dict["track_id"] = track_id
    params_dict["apikey"] = apikey
    unique_ident = unique_i(baseurl, params_dict, mtype)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        musix_response = requests.get(baseurl + mtype, params_dict)
        musix_text = musix_response.text
        CACHE_DICTION[unique_ident] = json.loads(musix_text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        f = open(CACHE_FNAME, "w")
        f.write(dumped_json_cache)
        f.close()
        return CACHE_DICTION[unique_ident]

# musix_lyrics_json_list = []
# for ele in track_id_list:
#     musix_lyrics_json = get_lyrics(ele)
#     musix_lyrics_json_list.append(musix_lyrics_json)
# print(musix_lyrics_json)

class Lyrics():
    def __init__(self, lyrics_dict={}):
        self.lyrics_body = lyrics_dict["lyrics"]["lyrics_body"]

def prettify_lyrics(lyrics_raw):
    lyrics_str = ""
    musix_lyrics_json = lyrics_raw["message"]["body"]
    if (type(musix_lyrics_json) == dict):
        musix_lyrics_text = Lyrics(musix_lyrics_json).lyrics_body
        lyrics_str += musix_lyrics_text
    elif (type(musix_lyrics_json) == list):
        for ele in musix_lyrics_json:
            musix_lyrics_text = Lyrics(musix_lyrics_json).lyrics_body
            lyrics_str += musix_lyrics_text
    return lyrics_str

# lyrics_str = ""
# for ele in musix_lyrics_json_list:
#     musix_lyrics_json = ele["message"]["body"]
#     if (type(musix_lyrics_json) == dict):
#         musix_lyrics_text = Lyrics(musix_lyrics_json).lyrics_body
#         lyrics_str += musix_lyrics_text
#     elif (type(musix_lyrics_json) == list):
#         for ele in musix_lyrics_json:
#             musix_lyrics_text = Lyrics(musix_lyrics_json).lyrics_body
#             lyrics_str += musix_lyrics_text
#
# f = open("lyrics.json", "w")
# f.write(lyrics_str)
# f.close()

# print(lyrics_str)

def track_search(name):
    baseurl = "http://api.musixmatch.com/ws/1.1/"
    mtype = "track.search?"
    params_dict = {}
    params_dict["q_artist"] = name
    params_dict["apikey"] = apikey
    unique_ident = unique_i(baseurl, params_dict, mtype)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        musix_response = requests.get(baseurl + mtype, params_dict)
        musix_text = musix_response.text
        CACHE_DICTION[unique_ident] = json.loads(musix_text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        f = open(CACHE_FNAME, "w")
        f.write(dumped_json_cache)
        f.close()
        return CACHE_DICTION[unique_ident]

def track_get(track_id):
    baseurl = "http://api.musixmatch.com/ws/1.1/"
    mtype = "track.get?"
    params_dict = {}
    params_dict["track_id"] = track_id
    params_dict["apikey"] = apikey
    unique_ident = unique_i(baseurl, params_dict, mtype)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        musix_response = requests.get(baseurl + mtype, params_dict)
        musix_text = musix_response.text
        CACHE_DICTION[unique_ident] = json.loads(musix_text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        f = open(CACHE_FNAME, "w")
        f.write(dumped_json_cache)
        f.close()
        return CACHE_DICTION[unique_ident]

def genre_distribution(track_list):
    genre_total = []
    for ele in track_list:
        track = track_search(ele)
        track_result = track['message']['body']['track_list']
        if track_result == []:
            track_id = 'missing'
        else:
            track_id = track_result[0]['track']['track_id']
        # album_name = track['message']['body']['track_list'][0]['track']['album_name']
        # artist_name = track['message']['body']['track_list'][0]['track']['artist_name']
        print(track_id)
        # print(album_name)
        # print(artist_name)
        if track_id != 'missing':
            track_result = track_get(track_id)
            genre_list = track_result['message']['body']['track']['primary_genres']['music_genre_list']
            if genre_list == []:
                genre = 999
            else:
                genre = genre_list[0]['music_genre']['music_genre_name']
                genre_total.append(genre)
    return genre_total

def genre_count(genre_list):
    genre_dict = {}
    for ele in genre_list:
        if ele not in genre_dict:
            genre_dict[ele] = 1
        else:
            genre_dict[ele] += 1
    genre_keys = genre_dict.keys()
    genre_name = []
    genre_count = []
    for ele in genre_keys:
        genre_name.append(ele)
        genre_count.append(genre_dict[ele])
    return genre_name, genre_count
