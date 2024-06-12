import csv
from time import sleep

import requests
from bs4 import BeautifulSoup

GET_DATA = False

BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"

name = None
email = None

headers = {'User-Agent': f'{name} ({email})'}

if GET_DATA:
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    html_doc = response.text
    with open('countries.html', 'w', encoding="utf-8") as file:
        file.write(html_doc)
else:
    with open('countries.html', 'r', encoding="utf-8") as file:
        html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')
table = soup.find('table', class_='wikitable')

countries = []

rows = table.find_all('tr')
for row in rows:
    name_col = row.th
    link = name_col.a
    if link is None:
        continue
    name = link.string
    date_joined = row.td.span.string
    country = {
        'Name': name,
        'Date joined': date_joined,
        'URL': BASE_URL + link['href'],
    }
    countries.append(country)

errors = {}

for country in countries[:3]:
    url = country['URL']
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        error = f"Response of {response.status_code} for {url}"
        errors[country['Name']] = error
        continue
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    latitude = soup.find('span', class_='latitude').string
    longitude = soup.find('span', class_='longitude').string

    country['Latitude'] = latitude
    country['Longitude'] = longitude
    sleep(0.5)

print(countries)
print(len(countries))

with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=['Name', 'Date joined', 'Latitude', 'Longitude', 'URL'])
    writer.writeheader()
    writer.writerows(countries)
