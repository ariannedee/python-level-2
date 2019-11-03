import csv
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org/"
URL = BASE_URL + "wiki/Member_states_of_the_United_Nations"

# Todo: Update with your info
name = None
email = None
assert name and email

headers = {'User-Agent': f'{name} ({email})'}
html_doc = requests.get(URL, headers=headers).text
soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', attrs={'class': 'wikitable'})

country_links = {}
for row in table.find_all('tr'):
    columns = row.find_all('td')
    if len(columns) > 0:
        country_data = columns[1]

        # Clean name
        country_name = country_data.text.strip()
        country_name = country_name.split('[')[0]

        # Get link to country page
        country_links[country_name] = BASE_URL + country_data.find('a').get('href')

print(country_links)


def get_population(table):
    tr = table.find('tr', attrs={'class': 'mergedtoprow'}, string='Population')
    text = tr.next_sibling.find('td').text
    return text.strip().split('[')[0]


def get_area(table):
    tr = table.find('tr', attrs={'class': 'mergedtoprow'}, string='Area ')
    text = tr.next_sibling.find('td').text
    return text.split('\xa0')[0].split('[')[0]


country_data = []

for country in country_links:
    url = country_links[country]
    html_doc = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.find('table', attrs={'class': 'geography'})
    country_dict = {
        'Name': country,
        'Population': get_population(table),
        'Area (km2)': get_area(table)
    }
    country_data.append(country_dict)
    time.sleep(0.1)

print(country_data)

with open('countries.csv', 'w') as output:
    writer = csv.DictWriter(output, ['Name', 'Population', 'Area (km2)'])
    writer.writeheader()
    writer.writerows(country_data)
