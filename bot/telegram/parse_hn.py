from bs4 import BeautifulSoup
import requests

def parse_hn():
    """Parse top 5 results from Hacker News"""

    hn = requests.get("https://news.ycombinator.com/").text
    soup = BeautifulSoup(hn, 'html.parser')
    new_posts = soup.find_all("a", class_="storylink")

    return {new_posts[i].get_text(): new_posts[i].get("href") for i in range(5)}


