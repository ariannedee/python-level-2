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
assert response.status_code == 200

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

country_dicts = []

table = soup.find('table', attrs={"class": "wikitable"})
rows = table.find_all('tr')
for row in rows:
    if row.td:
        tds = row.find_all('td')
        # Get the name
        links = tds[0].find_all('a')
        name = links[1].string
        # Get the URL
        url = links[1]['href']
        # Get the date joined
        date_joined = tds[1].span.string

        country_dict = {
            'Name': name,
            'URL': BASE_URL + url,
            'Date Joined': date_joined
        }
        country_dicts.append(country_dict)

assert len(country_dicts) > 100


def get_area():
    tr = table.find('tr', string="Area ").next_sibling
    area = tr.td.text.strip()
    return area.split('[')[0].split('\xa0')[0]


def get_population():
    tr = table.find('tr', string="Population").next_sibling
    population = tr.td.text.strip()
    return population.split('[')[0].split(" ")[0]


for country_dict in country_dicts[:5]:
    response = requests.get(country_dict['URL'])
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.table

    # Add new data to dict
    country_dict['Area'] = get_area()
    country_dict['Population'] = get_population()

    # Only make requests as fast as a human could click links
    time.sleep(1)

print(country_dicts)
with open('countries.csv', 'w') as file:
    # extrasaction=ignore ignores the URL field
    writer = csv.DictWriter(file, ('Name', 'Date Joined', 'Area', 'Population'), extrasaction='ignore')

    writer.writeheader()
    writer.writerows(country_dicts)
