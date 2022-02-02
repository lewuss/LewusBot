import requests
import json
import instaloader
from instagramkeys import *
from datetime import datetime, date

"""L = instaloader.Instaloader()
L.login(user, password)"""

BASE_URL = 'https://api.twitch.tv/helix/'
authURL = 'https://id.twitch.tv/oauth2/token'

keys = open("newkeys.txt", 'r')

CLIENT_ID = keys.readline().strip()
token = keys.readline().strip()
oauth = keys.readline().strip()

INDENT = 2

AutParams = {'client_id': CLIENT_ID,
             'client_secret': token,
             'grant_type': 'client_credentials'
             }

AUTCALL = requests.post(url=authURL, params=AutParams)
ACCESS_TOKEN = AUTCALL.json()['access_token']
HEADERS = {'Client-ID': CLIENT_ID, 'Authorization': "Bearer " + ACCESS_TOKEN}


def get_response(query):
    url = BASE_URL + query
    response = requests.get(url, headers=HEADERS)
    return response


def print_response(response):
    response_json = response.json()
    print(json.dumps(response_json, indent=INDENT))


def get_stream_info_query(user_login):
    return 'streams?user_login={0}'.format(user_login)


def get_user_streams_query(user_login):
    return 'streams?user_login={0}'.format(user_login)


def get_channels_info_query(user_login):
    user_id = get_user_id(user_login)
    return f'channels?broadcaster_id={user_id}'


def get_user_name_query(user_id):
    return f'users?id={user_id}'


def get_streams_all(language, pagination):
    return f'streams?first=100&language={language}&after={pagination}'


def get_user_query(user_login):
    return 'users?login={0}'.format(user_login)


def test_query(user_login):
    return f'moderation/moderators?broadcaster_id={get_user_id(user_login)}'


def get_follows_query(user_id, pagination):
    return f'users/follows?from_id={user_id}&first=100&after={pagination}'


def get_followers_query(user_id, pagination):
    return f'users/follows?to_id={user_id}&first=100&after={pagination}'


def get_top_streams_query(top, language):
    return f'streams?first={top}&language={language}'


def get_check_if_follows_query(user_follows, user_followed):
    return 'users/follows?from_id={0}&to_id={1}'.format(get_user_id(user_follows), get_user_id(user_followed))


def get_all_chatters(channel):
    url = f'http://tmi.twitch.tv/group/user/{channel.lower()}/chatters'
    try:
        all_chatters = requests.get(url).json()['chatters']
        chatters = all_chatters['staff'] + all_chatters['global_mods'] + all_chatters['admins'] \
                   + all_chatters['moderators'] + all_chatters['vips'] + all_chatters['viewers']
        chatters = sorted(chatters)
        return chatters
    except:
        print(channel)


def user_info(user_login):
    query = get_user_query(user_login)
    response = get_response(query)
    if response.ok:
        return response.json()
    return False


def streams_info(user_login):
    query = get_user_streams_query(user_login)
    response = get_response(query)
    return response.json()


def is_partnered(user_login):
    query = get_user_query(user_login)
    response = get_response(query)
    response_json = response.json()
    partner = response_json['data'][0]['broadcaster_type']
    print(partner)


def get_user_id(user_login):
    query = get_user_query(user_login)
    response = get_response(query)
    response_json = response.json()
    User_ID = response_json['data'][0]['id']
    return (User_ID)


def check_if_live(user_login):
    query = get_stream_info_query(user_login)
    try:
        response = get_response(query)
        response_json = response.json()
        is_live = response_json['data'][0]['type']
        if is_live == "live":
            return True
        else:
            return False
    except:
        return False


def get_chatters(user_login):
    url = f'http://tmi.twitch.tv/group/user/{user_login.lower()}/chatters'
    return requests.get(url).json()['chatter_count']


def get_amount_of_viewers_from_top_streams(top, language):
    query = get_top_streams_query(top, language.lower())
    response = get_response(query).json()
    viewers = 0
    for users in response['data']:
        viewers += users['viewer_count']
    return viewers


def get_number_of_streamers(language):
    cursor = ""
    query = get_streams_all(language, cursor)
    response = get_response(query).json()
    num_of_streams = len(response['data'])
    pagination = response['pagination']
    while pagination:
        cursor = pagination['cursor']
        query = get_streams_all(language, cursor)
        response = get_response(query).json()
        pagination = response['pagination']
        num_of_streams += len(response['data'])
    return num_of_streams


def get_names_of_top_streams(language, top):
    cursor = ""
    streamers = []
    for x in range(top // 100):
        query = get_streams_all(language, cursor)
        response = get_response(query).json()
        for streams in response['data']:
            streamers.append(streams['user_login'])
        try:
            cursor = response['pagination']['cursor']
        except:
            return streamers
    return streamers


def get_viewers(user_login):
    return streams_info(user_login)['data'][0]['viewer_count']


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y/%m/%d")
    return abs((d2 - d1).days)


def check_if_x_follows_y(X, Y):
    query = get_check_if_follows_query(X, Y)
    response = get_response(query)
    response_json = response.json()
    try:
        Date = response_json['data'][0]['followed_at'][0:10]
        today = date.today().strftime("%Y/%m/%d")
        datediff = days_between(Date, today)
        return f"{X} follows {Y} since {Date} ({datediff} days)"
    except:
        return X + " doesn't follow " + Y


def denciak_check(X, Y):
    query = get_check_if_follows_query(X, Y)
    response = get_response(query)
    response_json = response.json()
    try:
        Date = response_json['data'][0]['followed_at'][0:10]
        today = date.today().strftime("%Y/%m/%d")
        datediff = days_between(Date, today)
        if datediff > 620:
            return f'{X} nie jest denciakiem'
        else:
            return f'{X} jest denciakiem'
    except:
        return X + " nie followuje " + Y + " i jest giga denciakiem."


def who_is_watching_famous(channel):
    chatters = get_all_chatters(channel)
    kto = []
    for x in Users:
        if x in chatters:
            kto.append(x)
    return kto


def who_is_watching_mental(channel):
    chatters = get_all_chatters(channel)
    kto = []
    for x in mentals:
        if x in chatters:
            kto.append(x)
    return kto


def is_mod(user_name, channel):
    url = f'http://tmi.twitch.tv/group/user/{channel.lower()}/chatters'
    try:
        all_chatters = requests.get(url).json()['chatters']
        mods = all_chatters['moderators'] + all_chatters['broadcaster'] \
               + all_chatters['global_mods']
        return user_name in mods
    except:
        return False


def is_vip(user_name, channel):
    url = f'http://tmi.twitch.tv/group/user/{channel.lower()}/chatters'
    try:
        all_chatters = requests.get(url).json()['chatters']
        vips = all_chatters['vips'] + all_chatters['broadcaster'] \
               + all_chatters['global_mods']
        return user_name in vips
    except:
        return False


def get_last_ig_foto(ig_name):
    ig_url = f'https://www.instagram.com/{ig_name.lower()}/channel/?__a=1'
    response = requests.get(ig_url, headers={'User-Agent': 'My User Agent 1.0'}).json()
    print(response)
    link = response['graphql']['user']['edge_owner_to_timeline_media']['edges'][0]['node']['shortcode']
    return f'https://instagram.com/p/{link}'


def get_last_ig_foto_instaloader(ig_name):
    profile = instaloader.Profile.from_username(L.context, ig_name)
    posts = profile.get_posts()
    print(dir(posts))
    for shortcode in posts:
        return f'https://www.instagram.com/p/{shortcode.shortcode}'


def get_all_follows(user_id):
    pagination = ''
    follows = []
    query = get_follows_query(user_id, pagination)
    response = get_response(query).json()
    total = response['total']
    for data in response['data']:
        follows.append(data['to_id'])
    if total % 100 == 0:
        times = int(total / 100) - 1
    else:
        times = total // 100
    for x in range(times):
        pagination = response['pagination']['cursor']
        query = get_follows_query(user_id, pagination)
        response = get_response(query).json()
        for data in response['data']:
            follows.append(data['to_id'])
    return follows


def get_all_followers(user_id):
    pagination = ''
    follows = []
    query = get_followers_query(user_id, pagination)
    response = get_response(query).json()
    total = response['total']
    for data in response['data']:
        follows.append(data['from_login'])
    if total % 100 == 0:
        times = int(total / 100) - 1
    else:
        times = total // 100
    for x in range(times):
        print(f'przejście {x} zrobione.')
        pagination = response['pagination']['cursor']
        query = get_followers_query(user_id, pagination)
        response = get_response(query).json()
        for data in response['data']:
            follows.append(data['from_login'])
    return follows


def get_all_new_followers(user_id):
    pagination = ''
    follows = []
    query = get_followers_query(user_id, pagination)
    response = get_response(query).json()
    for data in response['data']:
        follows.append(data['from_name'])
    month = 8
    while month == 8:
        print(f'przejście zrobione.')
        pagination = response['pagination']['cursor']
        query = get_followers_query(user_id, pagination)
        response = get_response(query).json()
        for data in response['data']:
            follows.append(data['from_name'])
            month = int(data['followed_at'][6])
    return follows


def get_user_name_from_id(user_id):
    query = get_user_name_query(user_id)
    response = get_response(query).json()
    return response['data'][0]['display_name']


def get_delay(user_name):
    query = get_channels_info_query(user_name)
    response = get_response(query).json()
    return response['data'][0]['delay']
file = open("znaniusers.txt", "r")
Users = []
for x in file:
    if x.endswith("\n"):
        StreamersName = x[:-1]
    else:
        StreamersName = x
    StreamersName = StreamersName.lower()
    Users.append(StreamersName)

mentals = []
file1 = open('mentals.txt', 'r')
for line in file1:
    mentals.append(line.strip())
