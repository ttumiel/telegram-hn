from bs4 import BeautifulSoup
import requests

def parse_hn(number=5, site=""):
    """Parse top 5 results from Hacker News"""
    number=5 if number>30 or number<1
    hn = requests.get("https://news.ycombinator.com/" + site).text
    soup = BeautifulSoup(hn, 'html.parser')
    new_posts = soup.find_all("a", class_="storylink")

    return [(new_posts[i].get_text(), new_posts[i].get("href")) for i in range(number)]


