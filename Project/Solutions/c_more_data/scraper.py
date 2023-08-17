import csv
import time

import requests
from bs4 import BeautifulSoup

GET_DATA = False
WRITE_DATA = True

BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"

name = None
email = None
headers = {'User-Agent': f'{name} ({email})'}

if GET_DATA:
    response = requests.get(URL, headers=headers)

    response.raise_for_status()

    with open('wikipedia.html', 'w', encoding="utf-8") as file:
        html_doc = response.text
        file.write(html_doc)
else:
    with open('wikipedia.html', 'r') as file:
        html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')
table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')

countries = []
for row in rows:
    name_link = row.th.a
    if not name_link:  # Header row
        continue

    name = name_link.string
    date = row.td.span.string
    link = name_link['href']
    country = {
        'Name': name,
        'Date Joined': date,
        'URL': BASE_URL + link,
    }
    countries.append(country)

for country in countries:
    response = requests.get(country['URL'], headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    latitude = soup.find('span', class_='latitude')
    if latitude:
        country['Latitude'] = latitude.string
        country['Longitude'] = soup.find('span', class_='longitude').string
    else:
        print(f"Not latitude/longitude for {country['Name']}: {country['URL']}")

    time.sleep(0.5)  # Simulate a human clicking links

if WRITE_DATA:
    with open('countries_more.csv', 'w') as file:
        writer = csv.DictWriter(file, ['Name', 'Date Joined', 'URL', 'Latitude', 'Longitude'], extrasaction='ignore')
        writer.writeheader()
        writer.writerows(countries)
