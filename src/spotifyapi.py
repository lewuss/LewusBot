import requests
import json
import time
from spotifykeys import *

TOKEN = {}
HEADERS = {}
for user in refresh_token:
    TOKEN[user] = refresh(user)
    HEADERS[user] = {"Content-Type": "application/json",
                     "Authorization": f"Bearer {TOKEN[user]}"
                     }

BASE_URL = 'https://api.spotify.com/v1/'


class Song:
    def __init__(self, id, artist, title, length, added_by):
        self.id = id
        self.artist = artist
        self.title = title
        self.length = length
        self.added_by = added_by


def update_headers(TOKEN, channel):
    global HEADERS
    HEADERS[channel] = {"Content-Type": "application/json",
                        "Authorization": f"Bearer {TOKEN}"
                        }


def get_response(query, type, channel):
    if type == "get":
        response = requests.get(query, headers=HEADERS[channel])
    elif type == "put":
        response = requests.put(query, headers=HEADERS[channel])
    elif type == "post":
        response = requests.post(query, headers=HEADERS[channel])
    global TOKEN
    if response.ok:
        return response
    else:
        TOKEN[channel] = refresh(channel)
        update_headers(TOKEN[channel], channel)
        get_response(query, type, channel)


def get_current_track_name(channel):
    query = f'{BASE_URL}me/player/currently-playing'
    response = get_response(query, 'get', channel).json()
    artist = response['item']['album']['artists'][0]['name']
    title = response['item']['name']
    song_name = f'{artist} - {title}'
    return song_name


def get_current_track_data(channel):
    query = f'{BASE_URL}me/player/currently-playing'
    response = get_response(query, 'get', channel).json()
    artist = response['item']['album']['artists'][0]['name']
    title = response['item']['name']
    song_id = response['item']['id']
    return song_id, artist, title,


def get_length(track_id, channel):
    query = f'{BASE_URL}tracks/{track_id}'
    response = get_response(query, 'get', channel).json()
    duration = response['duration_ms']
    return duration


def get_current_track_id(channel):
    query = f'{BASE_URL}me/player/currently-playing'
    response = get_response(query, 'get', channel).json()
    song_id = response['item']['id']
    return song_id


def pause(channel):
    query = f'{BASE_URL}me/player/pause'
    response = get_response(query, 'put', channel)


def play(channel):
    query = f'{BASE_URL}me/player/play'
    response = get_response(query, 'put', channel)


def find_song(search_terms, channel):
    query = f'{BASE_URL}search?q={search_terms}&type=track'
    response = get_response(query, 'get', channel).json()
    artist = response['tracks']['items'][0]['artists'][0]['name']
    title = response['tracks']['items'][0]['name']
    spotify_id = response['tracks']['items'][0]['id']
    return artist, title, spotify_id


def skip(channel):
    query = f'{BASE_URL}me/player/next'
    response = get_response(query, 'post', channel)


def add_to_que(arist, title, track_id, channel):
    track_id = f"spotify:track:{track_id}"
    query = f'{BASE_URL}me/player/queue?uri={track_id}'
    get_response(query, 'post', channel)


def change_volume(level, channel):
    query = f'{BASE_URL}me/player/volume?volume_percent={level}'
    response = get_response(query, 'put', channel)


def get_current_playback_state(channel):
    query = f'{BASE_URL}me/player'
    response = get_response(query, 'get', channel).json()
    return response['is_playing']


def get_current_volume(channel):
    query = f'{BASE_URL}me/player'
    return get_response(query, 'get', channel).json()['device']['volume_percent']
