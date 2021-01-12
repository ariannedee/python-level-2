import csv
from time import sleep

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

table = soup.find('table', class_="wikitable")
rows = table.find_all('tr')

country_dicts = []
for row in rows:
    columns = row.find_all('td')
    if len(columns) > 0:
        name_link = columns[0].find_all('a')[1]
        name = name_link.string
        url = name_link['href']
        date_joined = columns[1].span.string
        country_dict = {
            'Name': name,
            'Date Joined': date_joined,
            'URL': BASE_URL + url
        }
        country_dicts.append(country_dict)


def get_area(table):
    tr = table.find('tr', string="Area ").next_sibling
    area = tr.td.text.strip()
    return area.split('[')[0].split('\xa0')[0]


def get_population(table):
    tr = table.find('tr', string="Population").next_sibling
    population = tr.td.text.strip()
    return population.split('[')[0].split(" ")[0]


for country_dict in country_dicts[:3]:
    url = country_dict['URL']
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        break

    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.table

    # Add new data to dict
    country_dict['Area'] = get_area(table)
    country_dict['Population'] = get_population(table)
    sleep(1)

with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, ['Name', 'Date Joined', 'Area', 'Population'], extrasaction="ignore")
    writer.writeheader()
    writer.writerows(country_dicts)
