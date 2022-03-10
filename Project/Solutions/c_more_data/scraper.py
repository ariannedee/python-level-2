import csv
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"

# Todo: Update with your info
name = None
email = None
assert name and email

# Dictionary of HTTP headers
headers = {'User-Agent': f'{name} ({email})'}

response = requests.get(URL, headers=headers)
response.raise_for_status()
html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

countries = []

table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    if not cols:
        continue
    name_col = cols[0]
    name = name_col.a['title']
    date = cols[1].text.strip()
    country = {
        'Name': name,
        'Date Joined': date,
        'URL': BASE_URL + name_col.a['href']
    }
    countries.append(country)

error_countries = []
for country_dict in countries[:10]:
    response = requests.get(country_dict['URL'], headers=headers)
    if response.status_code != 200:
        error_countries.append(country_dict)
        continue
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    lat = soup.find('span', class_='latitude').text
    lon = soup.find('span', class_='longitude').text
    if not lat or not lon:
        error_countries.append(error_countries)
    country_dict['Latitude'] = lat
    country_dict['Longitude'] = lon
    time.sleep(0.5)

print(error_countries)

with open('data/countries_2.csv', 'w') as file:
    writer = csv.DictWriter(file, ['Name', 'Date Joined', 'Latitude', 'Longitude'], extrasaction='ignore')
    writer.writeheader()
    writer.writerows(countries)
