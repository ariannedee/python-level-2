import csv
from time import sleep

import requests
from bs4 import BeautifulSoup

LOAD_DATA = False

BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"

if LOAD_DATA:
    response = requests.get(URL)
    print(response.status_code)
    response.raise_for_status()
    html_doc = response.text

    with open('wikipedia.html', 'w', encoding="utf-8") as file:
        file.write(html_doc)
else:
    with open('wikipedia.html', encoding="utf-8") as file:
        html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')
countries = []
for row in rows:
    name_col = row.th
    name_link = name_col.a
    if name_link is None:  # Header
        continue
    name = name_link.string
    date_of_admission = row.td.text.strip().split('[')[0]
    country = {
        'Name': name,
        'Date of admission': date_of_admission,
        'URL': name_link['href'],
    }
    countries.append(country)

for country in countries[:3]:
    url = BASE_URL + country['URL']
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Error getting {country["Name"]} data from {url}')
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    country['Latitude'] = soup.find('span', class_='latitude').string
    country['Longitude'] = soup.find('span', class_='longitude').string
    sleep(0.5)

with open('countries.csv', 'w', encoding='UTF-8') as file:
    writer = csv.DictWriter(file, ('Name', 'Date of admission', 'URL', 'Latitude', 'Longitude'))
    writer.writeheader()
    writer.writerows(countries)
