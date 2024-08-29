from bs4 import BeautifulSoup
import requests
import re

number = 7838
url = f'https://scp-wiki.wikidot.com/scp-{number}'

soup = BeautifulSoup(requests.get(url).content, 'html.parser')
txt = "\n".join(soup.text.splitlines()[219:])

with open("text.txt","w",encoding="utf-8") as f:
    f.write(txt)