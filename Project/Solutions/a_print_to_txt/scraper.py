import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

name = None
email = None

assert name and email, "Please supply your name and email"

headers = {"User-Agent": f"{name} ({email})"}
response = requests.get(URL, headers=headers)

response.raise_for_status()

html_doc = response.text

soup = BeautifulSoup(html_doc, "html.parser")

table = soup.find("table", class_="wikitable")

countries = []
for row in table.find_all("tr"):
    name_link = row.th.a
    if not name_link:
        continue
    name: str = name_link.string
    name = name.split(" (")[0]
    countries.append(name)

with open("countries.txt", "w") as file:
    file.write("\n".join(countries))