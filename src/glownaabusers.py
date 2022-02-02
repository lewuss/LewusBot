import requests
import json
import pymongo

CLIENT_ID = 'kimne78kx3ncx6brgo4mv6wki5h1ko'
URL = 'https://gql.twitch.tv/gql'
client = pymongo.MongoClient(
    f"mongodb+srv://twitchdata:zenek123@cluster0.qtyar.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


def get_chatters(user_login):
    url = f'http://tmi.twitch.tv/group/user/{user_login.lower()}/chatters'
    return requests.get(url).json()['chatter_count']


def get_featured_streams():
    query = """query {
            featuredStreams(language: "pl", first: 8) {
            description
            priorityLevel
            stream {
                broadcaster {
                    displayName
                    id
                    login
                }
            viewersCount
            }
        }}"""

    HEADERS = {'Client-ID': CLIENT_ID,
               "Content-Type": "application/json"
               }
    response = requests.post(URL, json={"query": query}, headers=HEADERS).json()
    glowna = []
    for stream in response['data']['featuredStreams']:
        user_info = {
            'user_login': stream['stream']['broadcaster']['displayName'],
            'viewers': stream['stream']['viewersCount'],
            'priorityLevel': stream['priorityLevel']
        }
        glowna.append(user_info)
    return glowna


def update_db(info):
    pass

