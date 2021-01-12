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

table = soup.find('table', class_="wikitable")
rows = table.find_all('tr')

country_dicts = []
for row in rows:
    columns = row.find_all('td')
    if len(columns) > 0:
        name_col = columns[0]
        name = name_col.find_all('a')[1].string
        date_joined = columns[1].span.string
        country_dict = {
            'Name': name,
            'Date Joined': date_joined
        }
        country_dicts.append(country_dict)

with open('data/countries.csv', 'w') as file:
    writer = csv.DictWriter(file, ['Name', 'Date Joined'])
    writer.writeheader()
    writer.writerows(country_dicts)
