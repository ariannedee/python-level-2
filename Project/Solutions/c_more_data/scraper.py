import csv
import time

import requests
from bs4 import BeautifulSoup
from requests import Response

SLEEP_SECS = 0.5

start = time.time()
BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"

# Todo: Update with your info
name = None
email = None
assert name and email

headers = {'User-Agent': f'{name} ({email})'}
response: Response = requests.get(URL, headers=headers)
response.raise_for_status()
html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')
table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')

countries = []
for row in rows[1:]:
    name_col = row.th
    link = name_col.a
    name = link.string
    country_url = link['href']
    date_joined = row.td.span.string.strip()
    country: dict = {
        'Name': name,
        'Date joined': date_joined,
        'URL': BASE_URL + country_url,
    }
    countries.append(country)

for country in countries[:]:
    country_url = country['URL']
    response: Response = requests.get(country_url, headers=headers)
    if response.status_code != 200:
        print(f"[WARNING] Couldn't get {country_url}")
        continue
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    try:
        latitude = soup.find('span', class_='latitude').string
        longitude = soup.find('span', class_='longitude').string
        country['Latitude'] = latitude
        country['Longitude'] = longitude
    except AttributeError:
        print(f"[WARNING] {country['Name']} doesn't have a latitude or longitude in {country_url}")
    time.sleep(SLEEP_SECS)

with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, ['Name', 'Date joined', 'URL', 'Latitude', 'Longitude'])
    writer.writeheader()
    writer.writerows(countries)

end = time.time()

print(f"Took {round(end - start, 1)}s to run ({round((end - start) // 60)}m {round((end - start) % 60)}s)")
