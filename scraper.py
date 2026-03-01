import sys
import requests
from bs4 import BeautifulSoup

# provide url
if len(sys.argv) < 2:
    print("not corrct format")
    sys.exit()

# take url
target_url = sys.argv[1]

# fetch the page
response = requests.get(target_url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

# title
if soup.title:
    print(soup.title.string)
else:
    print("No Title")

# body
print(soup.get_text())

# links
links = soup.find_all("a")
for l in links:
    href = l.get("href")
    if href:
        print(href)
