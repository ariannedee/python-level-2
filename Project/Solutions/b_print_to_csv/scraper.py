import csv

import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

# Todo: Update with your info
name = None
email = None
assert name and email

headers = {'User-Agent': f'{name} ({email})'}
response = requests.get(URL, headers=headers)
assert response.status_code == 200

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

country_dicts = []

table = soup.find('table', attrs={"class": "wikitable"})
rows = table.find_all('tr')
for row in rows:
    if row.td:
        tds = row.find_all('td')
        # Get the name
        links = tds[0].find_all('a')
        name = links[1].string
        # Get the date joined
        date_joined = tds[1].span.string

        country_dict = {
            'Name': name,
            'Date Joined': date_joined
        }
        country_dicts.append(country_dict)

assert len(country_dicts) > 100

with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, ('Name', 'Date Joined'))
    writer.writeheader()
    writer.writerows(country_dicts)
