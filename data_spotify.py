import json
import requests

# client_id = 'a0a03de7343147d6a0db32f5a6198646'
#
# baseurl = "https://accounts.spotify.com/authorize"
# params_dict = {}
# params_dict['client_id'] = client_id
# params_dict['type'] = 'code'
# params_dict['redirect_uri'] = 'http://localhost:8888'
# params_dict['scope'] = 'user-read-private user-read-email user-top-read'
# x = requests.get(baseurl, params_dict).text
# print(x)
#
# baseurl = "https://accounts.spotify.com/api/token"
# params_dict = {}
# params_dict['grant_type'] = 'authorization_code'
# params_dict['code'] = code
# params_dict['redirect_uri'] = 'http://localhost:8888'
# header = { 'Authorization': 'Basic ' + access_token }
# spotify_response =  requests.get(baseurl, params_dict, headers=header)



# access_token = input("Access_token: ")

CACHE_FNAME = "dataall_cache.json"
try:
    cache_file = open(CACHE_FNAME, "r")
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def unique_i(baseurl, params_dict):
    alphabetized_keys = params_dict.keys()
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params_dict[k]))
    return baseurl + "&".join(res)

# access_token = app.js.body.access_token
def get_top_artists(access_token):
    # access_token = access_token
    baseurl = "https://api.spotify.com/v1/me/top/artists"
    params_dict = {}
    params_dict['limit'] = 10
    #the max of limit is 50
    params_dict['time_range'] = 'long_term'
    header = { 'Authorization': 'Bearer ' + access_token }
    unique_ident = unique_i(baseurl, params_dict)
    if unique_ident in CACHE_DICTION:
        # print(CACHE_DICTION[unique_ident])
        return CACHE_DICTION[unique_ident]
    else:
        spotify_response =  requests.get(baseurl, params_dict, headers=header)
        spotify_text = spotify_response.text
        # print(spotify_text)
        CACHE_DICTION[unique_ident] = json.loads(spotify_text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        f = open(CACHE_FNAME, "w")
        f.write(dumped_json_cache)
        f.close()
        return CACHE_DICTION[unique_ident]

class Artist():
    def __init__(self, artist_obj={}):
        self.external_url = artist_obj['external_urls']['spotify']
        self.follower = artist_obj['followers']['total']
        self.genres = artist_obj['genres']
        self.name = artist_obj['name']
        self.popularity = artist_obj['popularity']

    def play(self):
        webbrowser.open(self.external_url)

# top_artists_json = get_top_artists()
def get_artist_list(top_artist_json):
    artist_list = []
    for ele in top_artist_json['items']:
        artist = Artist(ele)
        artist_name = artist.name
        artist_list.append(artist_name)
    return artist_list
# print(artists_list)
