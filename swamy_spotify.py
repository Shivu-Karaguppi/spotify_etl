import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import base64
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import aws_db as db
currentDateTime = datetime.datetime.now()
dateTime = currentDateTime.strftime("%d-%m-%y")
week_day = currentDateTime.strftime("%a")

client_id='f77396169db54abbbf875d54b1c473c7'
client_secret='fde71c32db2c4d1d85f801c8e8d4e7a0'

def access_token():
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')

    # Set up the authentication options
    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'headers': {
            'Authorization': 'Basic ' + credentials
        },
        'data': {
            'grant_type': 'client_credentials',
            'scope': "user-library-read playlist-modify-private",
        }
    }
    global headers
    

    # Make the POST request
    response = requests.post(**auth_options)

    if response.status_code == 200:
        global token
        token = response.json().get('access_token')
        print(f'Token: {token}')
        headers = {
        'Authorization': f'Bearer {token}',
        }
    return token

access_token()

def get_artist(artist_name):
        url = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1'
        response = requests.get(url, headers=headers)
        artist_data = response.json()

        id = artist_data['artists']['items'][0]['id']
        name = artist_data['artists']['items'][0]['name']
        followers = artist_data['artists']['items'][0]['followers']['total']
        try:
            genre = artist_data['artists']['items'][0]['genres'][0]
        except:
            genre = "NA"
        popularity = artist_data['artists']['items'][0]['popularity']
        print(id,name,followers,genre,popularity)

        redefined_artist_data = {"id": id,
                                 "name": name,
                                 "followers": followers,
                                 "genre": genre,
                                 "popularity": popularity}
        db.insert_records(id,name,followers,popularity,genre,dateTime,week_day)
        # print(redefined_artist_data)
        # return redefined_artist_data



# Authenticate with the Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Get the top artists on Spotify currently
top_artists = sp.category_playlists(category_id='toplists')['playlists']['items'][0]
tracks = sp.playlist_tracks(top_artists['id'])['items']

artists_today = []

for track in tracks:
    artist = track['track']['artists'][0]['name']
    if artist not in artists_today:
        artists_today.append(artist)
    if len(artists_today) == 10:
        break

print("Top 10 Artists on Spotify today:")
for i, artist in enumerate(artists_today, start=1):
    print(f"{i}. {artist}")
    get_artist(artist)





