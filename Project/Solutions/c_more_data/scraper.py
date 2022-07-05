import time

import requests
from bs4 import BeautifulSoup
from csv import DictWriter

BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"

# Todo: Update with your info
name = None
email = None
assert name and email

headers = {'User-Agent': f'{name} ({email})'}

response = requests.get(URL, headers=headers)

assert response.status_code == 200, f"Got {response.status_code}: {response.reason}"

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')

country_dicts = []
rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    if len(cols) > 0:
        name_col = cols[0]
        name_str: str = name_col.text
        name = name_str.split('[')[0].strip()
        date_joined = cols[1].text.strip()
        url = name_col.a['href']
        country_dict = {
            'Name': name,
            'Date Joined': date_joined,
            'URL': BASE_URL + url,
        }
        country_dicts.append(country_dict)

for country_dict in country_dicts[:10]:
    response = requests.get(country_dict['URL'], headers=headers)  # Get the URL from the dictionary

    if response.status_code != 200:
        print(f"Error getting page for {country_dict['Name']}: {country_dict['URL']}")

    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    lat = soup.find('span', class_='latitude').string
    lon = soup.find('span', class_='longitude').string
    country_dict['Latitude'] = lat
    country_dict['Longitude'] = lon
    time.sleep(0.5)  # Pause to avoid too frequent requests

with open('data/countries.csv', 'w') as file:
    writer = DictWriter(file, fieldnames=['Name', 'Date Joined', 'URL', 'Latitude', 'Longitude'], extrasaction='ignore')
    writer.writeheader()
    writer.writerows(country_dicts)
