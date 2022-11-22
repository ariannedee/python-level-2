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

headers = {'User-Agent': f'{name} ({email})'}

response = requests.get(URL, headers=headers)

response.raise_for_status()

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')[1:]
country_dicts = []
for row in rows:
    name = row.th.a.string
    url = BASE_URL + row.th.a['href']
    date_joined = row.td.span.string
    country_dict = {
        'Name': name,
        'Date Joined': date_joined,
        'URL': url,
    }
    country_dicts.append(country_dict)

for country in country_dicts[:3]:
    url = country['URL']
    response = requests.get(url, headers=headers)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    country['Latitude'] = soup.find('span', class_='latitude').string
    country['Longitude'] = soup.find('span', class_='longitude').string
    time.sleep(0.5)

with open("countries_more.csv", "w") as file:
    writer = csv.DictWriter(file, fieldnames=['Name', 'Date Joined', 'URL', 'Latitude', 'Longitude'])
    writer.writeheader()
    writer.writerows(country_dicts)
