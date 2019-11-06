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

countries = []
for row in table.find_all('tr'):
    columns = row.find_all('td')
    if len(columns) > 0:
        country_name = columns[1].text.strip()
        country_name = country_name.split('[')[0]
        date_joined = columns[2].text.strip()
        url = BASE_URL + columns[1].find('a').get('href')

        country_data = {
            'Name': country_name,
            'Date Joined': date_joined,
            'URL': url
        }
        countries.append(country_data)


def get_population(table):
    tr = table.find('tr', attrs={'class': 'mergedtoprow'}, string='Population')
    text = tr.next_sibling.find('td').text
    return text.strip().split('[')[0]


def get_area(table):
    tr = table.find('tr', attrs={'class': 'mergedtoprow'}, string='Area ')
    text = tr.next_sibling.find('td').text
    return text.split('\xa0')[0].split('[')[0]


for country in countries[:10]:
    url = country['URL']
    html_doc = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.find('table', attrs={'class': 'geography'})
    more_data = {
        'Population': get_population(table),
        'Area (km2)': get_area(table)
    }
    country.update(more_data)
    print(country)
    time.sleep(0.5)


with open('countries.csv', 'w') as output:
    writer = csv.DictWriter(output, ['Name', 'Date Joined', 'Population', 'Area (km2)'], extrasaction='ignore')
    writer.writeheader()
    writer.writerows(countries[:10])
