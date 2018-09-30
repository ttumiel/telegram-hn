from bs4 import BeautifulSoup
import requests

hn = requests.get("https://news.ycombinator.com/").text

soup = BeautifulSoup(hn, 'html.parser')
new_posts = soup.find_all("a", class_="storylink")

for i in range(5):
    print(new_posts[i].get("href"))
    print(new_posts[i].get_text())
    print()