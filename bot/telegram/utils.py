from bs4 import BeautifulSoup
import requests
from firebase_admin import db

def parse_hn(number=5, site=""):
    """
    Parse top 5 results from Hacker News
    Use firebase method instead
    """
    if number>30 or number<1: number=5
    hn = requests.get("https://news.ycombinator.com/" + site).text
    soup = BeautifulSoup(hn, 'html.parser')
    new_posts = soup.find_all("a", class_="storylink")

    return [(new_posts[i].get_text(), new_posts[i].get("href")) for i in range(number)]

def check_string_num(num):
    try:
        return int(num)
    except ValueError:
        return None

def parse_hn_firebase():
    """
    Parse Hacker News using the firebase API
    """

    # Get a database reference to our posts
    ref = db.reference('/v0/topstories.json', url='https://hacker-news.firebaseio.com')

    # Read the data at the posts reference (this is a blocking operation)
    print(ref.get())


