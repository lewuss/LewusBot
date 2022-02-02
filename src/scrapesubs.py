from bs4 import BeautifulSoup
import requests


def get_subs_from_tracker(channel):
    URL = f'https://twitchtracker.com/{channel.lower()}/subscribers'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        subs_counter = soup.find("span", {"class": "to-number"}).getText()
        return subs_counter
    except:
        return None
