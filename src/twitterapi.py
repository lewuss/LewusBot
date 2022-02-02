import tweepy
import json
import api

keys = open("keystwitter.txt", 'r')

CONSUMER_KEY = keys.readline().strip()
CONSUMER_SECRET = keys.readline().strip()
ACCESS_TOKEN = keys.readline().strip()
ACCESS_TOKEN_SECRET = keys.readline().strip()

TwitterAuth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
TwitterAuth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

tweeter = tweepy.API(TwitterAuth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_user_id_from_name(user_name):
    user = tweeter.get_user(user_name)
    return user.id_str


def find_last_tweet(user_id):
    tweets = tweeter.user_timeline(id=user_id, count=100)
    for tweet in tweets:
        if tweet.text[0] != '@':
            return tweet


def get_tweet_link_and_text(tweet):
    text = tweet.text
    id = tweet.id
    user_name = tweet.user.screen_name
    link = f'https://twitter.com/{user_name}/status/{id}'
    return text, link


def get_last_tweet(user_name):
    user_id = get_user_id_from_name(user_name)
    tweet = find_last_tweet(user_id)
    return get_tweet_link_and_text(tweet)


def get_followers_count(user_name):
    id = get_user_id_from_name(user_name)
    user = tweeter.get_user(id)
    return user.followers_count


def get_followers_list(screen_name):
    followers = []
    for follower in tweepy.Cursor(tweeter.followers_ids, screen_name=screen_name, count=5000).items():
        followers.append(follower)
    return followers


def get_followers_list_with_followers_count(screen_name):
    followers_id = get_followers_list(screen_name)
    info = []
    for i in range(0, len(followers_id), 100):
        try:
            chunk = followers_id[i:i + 100]
            batch_info = tweeter.lookup_users(user_ids=chunk)
            chunk_info = []
            for user in batch_info:
                chunk_info.append({
                    'name': user._json['screen_name'],
                    'followers_count': user._json['followers_count']
                })
            print(str(i // 100) + "loop zrobiony.")
            info.extend(chunk_info)
        except:
            import traceback
            traceback.print_exc()
            print('Something went wrong, skipping...')
    return info


def save_to_json(data, screen_name):
    with open(f'{screen_name}_followers.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_famous_followers(data):
    famous = []
    for user in data:
        if user['followers_count'] > 10000:
            famous.append(user)

    famous = sorted(famous, key=lambda k: k['followers_count'], reverse=True)

    for user in famous:
        print(user['name'], ' followers: ', user['followers_count'])


def get_follower_list_with_followers_count_pick_famous_and_save_to_json_please(screen_name):
    followers = get_followers_list_with_followers_count(screen_name)
    save_to_json(followers, screen_name)
    get_famous_followers(followers)

