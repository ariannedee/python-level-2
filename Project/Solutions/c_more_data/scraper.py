import csv
import logging
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"

name = None
email = None

assert name and email, "Fill in your name and email"

headers = {'User-Agent': f'{name} ({email})'}

response = requests.get(URL, headers=headers)
response.raise_for_status()

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

countries = []

table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')
for row in rows:
    name_column = row.th
    link = name_column.a
    if link:
        url = link['href']
        country_name = link.string
        date_of_admission = row.td.span.string
        country = {
            'Name': country_name,
            'Date of admission': date_of_admission,
            'URL': BASE_URL + url,
        }
        countries.append(country)

for country in countries[:3]:
    response = requests.get(country['URL'], headers=headers)
    if response.status_code != 200:
        logging.warning(f"Error getting page for {country['Name']} at {country['URL']}")
        continue
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    try:
        country['Latitude'] = soup.find('span', class_='latitude').string
        country['Longitude'] = soup.find('span', class_='longitude').string
    except AttributeError:
        logging.warning(f"Error getting lat and lon for {country['Name']} at {country['URL']}")
    time.sleep(0.5)

print(countries[0])

with open('countries_more.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=('Name', 'Date of admission', 'Latitude', 'Longitude'), extrasaction='ignore')
    writer.writeheader()
    writer.writerows(countries)
