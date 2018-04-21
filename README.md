# si-507-final-project
OVERVIEW

######################################################
Question1
Data sources used, including instructions for a user to access the data sources (e.g., API keys or client secrets needed, along with a pointer to instructions on how to obtain these and instructions for how to incorporate them into your program (e.g., secrets.py file format))

There are two API & a page scraping I have used in this project.
1 Spotify API
You can get the client_id & client_secret of Spotify from:
https://developer.spotify.com

2 Musixmatch API
You can get the api_key of Musixmatch from:
https://developer.musixmatch.com

3 Billboard top 100 tracks page scraping
https://www.billboard.com/charts/hot-100

After you got the first two api_key and client_id&secret, you can fill these into the file secrets_sample.py in the main repository. And then, change the name of it to secret.py

You are all set!

######################################################
Question2
Any other information needed to run the program (e.g., pointer to getting started info for plotly)

There are 3 steps to set up:
1 Go to the login repository, go to the spotify-auth repository, go to the authorization repository. Just like this when you in terminal:
cd login
cd spotify-auth
cd authorization

2 Authorize the Spotify API by putting in the code:
node app.js
After that, open the 'http://localhost:8888' in your browser.
Click the first button 'Log in with Spotify'
Authorize the application.
Finally, copy the access_token at the bottom.

3 Back to the main repository, like:
cd ../../../
And then, open the python file app.py

######################################################
Question3
Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.

1 Building database instead of initial it every time.
All of the data that related to Musixmatch API are being stored in the database, like lyrics, track, album, and artist. The requesting and storing process will need several mins, so instead of refresh the database every time when we activate the app.py, I put in a function '' using SQL to select the bands/artists' data we already have in the database. Just like using cache, this may save a lot of time.

CODE ->

2 Use Plotly offline library connect with Flask
Import plotly.graph_objs to draw the offline charts.
CODE ->app.py line62-67, 78-85, 87-96

3 Database structure
Instead of just link the data with only the higher level, like just involve track's info in the lyrics case. I involved all the info that has the higher hierarchy of the data, like involve track, album, and artist info in the lyrics case, involve album and artist info in the track case.

CODE ->data_database.py

4 Musixmatch search requests & Spotify user's top bands/artists requests
Request get data from these two APIs.
CODE ->musixmatch_request.py & data_spotify.py

######################################################
Question4
Brief user guide, including how to run the program and how to choose presentation options.

There are three sections you can play with:
1 Put in the specific band/artist name in the first text box.
i.e. you can put in: Megadeth, or Slayer, or Metallica, or Arch Enemy, or Extreme (these are the data that already been stored in the database)
After that, you can click any of the three to see the album release distribution, tracks' length distribution, and the most frequent used words in all of the tracks of this band.

2 Paste the access_token into the second text box.
Connect to your personal Spotify account, to see the top 10 bands you are listening. Click each band's name, you can see the most frequently used words for each band. Also, at the bottom of the page, you can also click the link to see the album and track length distribution.
*this may take a while, because the band in your account might not in the database, the application needs to request new data.*

3 See the Billboard's top 100 tracks' genre distribution
By clicking the button on the bottom, you can see the genre distribution and the list that been scraped from the Billboard webpage.
*actually, this may also take a few seconds. because the list is change everyday, so I put the data in the cache file. so if it's a new day, it may require new request.*
