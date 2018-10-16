from bs4 import BeautifulSoup
import requests
from firebase import firebase

OPTIONS=["top", "ask", "show", "job", "best", "new"]

OPTIONS_URL={"top":"", "ask":"ask", "show":"show", "job":"jobs", "best":"best", "new":"newest"}

def parse_hn(option, number):
    """
    Parse top 5 results from Hacker News
    Use firebase method instead
    """
    if number>30 or number<1: number=5
    hn = requests.get("https://news.ycombinator.com/" + OPTIONS_URL[option]).text
    soup = BeautifulSoup(hn, 'html.parser')
    new_posts = soup.find_all("a", class_="storylink")

    print(len(new_posts))

    return [(new_posts[i].get_text(), new_posts[i].get("href")) for i in range(number)]

def check_string_num(num):
    try:
        return int(num)
    except ValueError:
        return None

def parse_hn_firebase(option="top", number=5):
    """
    Parse Hacker News using the firebase API
    """
    fb = firebase.FirebaseApplication('https://hacker-news.firebaseio.com', None)

    if option in OPTIONS:
        post_ids = fb.get('/v0/' + option + 'stories', None)
    else:
        post_ids = fb.get('/v0/topstories', None)

    results = []
    for i in range(number):
        data = fb.get('/v0/item/' + str(post_ids[i]), None)
        results.append((data["title"], data["url"]))

    return results
