import csv

import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

# Todo: Update with your info
name = None
email = None
assert name and email

# Dictionary of HTTP headers
headers = {'User-Agent': f'{name} ({email})'}
response = requests.get(URL, headers=headers)

assert response.status_code == 200, f"Status code: {response.status_code}"

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find("table", class_="wikitable")

countries = []
for row in table.find_all("tr"):
    cols = row.find_all("td")
    if len(cols) > 0:
        name = cols[0].span.a['title']
        date_joined = cols[1].text.strip()
        country_dict = {
            "Name": name,
            "Date Joined": date_joined
        }
        countries.append(country_dict)

with open("data/countries.csv", "w") as file:
    writer = csv.DictWriter(file, ["Name", "Date Joined"], extrasaction="ignore")
    writer.writeheader()
    writer.writerows(countries)
