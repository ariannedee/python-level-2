import csv
from time import sleep

import requests

from bs4 import BeautifulSoup
from pprint import pprint

LOAD_DATA = False
BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"

if LOAD_DATA:
    response = requests.get(URL)
    response.raise_for_status()
    html_doc = response.text

    with open('countries.html', 'w', encoding="utf-8") as file:
        file.write(html_doc)
else:
    with open('countries.html', encoding="utf-8") as file:
        html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')

countries = []
for row in rows:
    th = row.th
    name_link = th.a
    if not name_link:  # header row
        continue
    name = name_link.string
    date_admitted = row.td.span.string
    country = {
        'Name': name,
        'Date admitted': date_admitted,
        'URL': BASE_URL + name_link['href'],
    }
    countries.append(country)

for country in countries[:2]:
    response = requests.get(country['URL'])
    if response.status_code != 200:
        print(f"Error on {country['URL']}, {response.status_code}: {response.reason}")
        continue
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    try:
        country['Latitude'] = soup.find('span', class_='latitude').string
        country['Longitude'] = soup.find('span', class_='longitude').string
    except Exception as e:
        print(f"Error getting details for {country['Name']} at {country['URL']}")
        print(repr(e))
    sleep(0.5)

pprint(countries)

with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=('Name', 'Date admitted', 'Latitude', 'Longitude', 'URL'))
    writer.writeheader()
    writer.writerows(countries)
