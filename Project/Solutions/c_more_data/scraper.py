import csv
import re
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

assert response.status_code == 200, f'Response got {response.status_code}'

html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')
table = soup.find('table', class_='wikitable')

countries = []
for row in table.find_all('tr'):
    name_column = row.find('td')
    if name_column:
        country_dict = {}
        name_link = name_column.find_all('a')[1]
        name = name_link.string
        country_dict['Name'] = name

        country_dict['URL'] = BASE_URL + name_link['href']

        date_column = row.find_all('td')[1]
        date_joined = date_column.span.text
        country_dict['Date Joined'] = date_joined

        countries.append(country_dict)


def get_area(table):
    # Look up 'Regular expressions'
    # Some pages have an extra space after "Area", so trying to find an exact match will fail.
    # re.compile("Area") creates a pattern to look for
    tr = table.find('tr', string=re.compile("Area *")).next_sibling
    area = tr.td.text.strip()
    return area.split('[')[0].split('\xa0')[0]


def get_population(table):
    tr = table.find('tr', string="Population").next_sibling
    population = tr.td.text.strip()
    return population.split('[')[0].split(" ")[0]


errors = []
for country_dict in countries:
    url = country_dict['URL']
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.table
    try:  # If any sub-page fails, skip it and keep track of it
        country_dict['Area'] = get_area(table)
        country_dict['Population'] = get_population(table)
    except AttributeError:
        errors.append(country_dict)
    sleep(1)  # Limit rate at which you request pages

if errors:  # Can investigate these pages further afterwards
    print(f'Error getting detail data from:')
    for country_dict in errors:
        print(f'  {country_dict["Name"]}: {country_dict["URL"]}')

with open('data/countries.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=('Name', 'Date Joined', 'Area', 'Population'), extrasaction='ignore')
    writer.writeheader()
    writer.writerows(countries)
