import csv
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://en.wikipedia.org'
URL = BASE_URL + '/wiki/Member_states_of_the_United_Nations'

response = requests.get(URL)
response.raise_for_status()

html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')

countries = []

for row in table.find_all('tr'):
    link = row.th.a
    if link is None:
        continue

    href = link['href']
    link_content: str = link.string
    name = link_content.split(' (')[0]
    date_joined = row.td.span.string

    country = {
        'Name': name,
        'Date joined': date_joined,
        'URL': href,
    }
    countries.append(country)

for country in countries[:3]:
    response = requests.get(BASE_URL + country['URL'])
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    country['Latitude'] = soup.find('span', class_='latitude').string
    country['Longitude'] = soup.find('span', class_='longitude').string
    time.sleep(0.5)

print(countries)

with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, ['Name', 'Date joined', 'Latitude', 'Longitude', 'URL'])
    writer.writeheader()
    writer.writerows(countries)
