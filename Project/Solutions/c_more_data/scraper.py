import csv
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org"
URL = f"{BASE_URL}/wiki/Member_states_of_the_United_Nations"

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

table = soup.find('table', attrs={'class': 'wikitable'})

countries = []
for row in table.find_all('tr'):
    tds = row.find_all('td')
    if len(tds) == 0:
        continue
    name_link = tds[0].a
    url = BASE_URL + name_link['href']
    name = name_link['title']
    date_joined = tds[1].text.strip()

    country_dict = {
        'Name': name,
        'Date Joined': date_joined,
        'URL': url,
    }
    countries.append(country_dict)

print(countries)

for country in countries[:3]:
    url = country['URL']
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    lat = soup.find('span', class_='latitude').text
    lon = soup.find('span', class_='longitude').text
    country['Latitude'] = lat
    country['Longitude'] = lon

    time.sleep(0.5)

with open('data/countries.csv', 'w') as file:
    writer = csv.DictWriter(file, ['Name', 'Date Joined', 'Latitude', 'Longitude'], extrasaction='ignore')
    writer.writeheader()
    writer.writerows(countries)
