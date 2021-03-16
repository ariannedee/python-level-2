import csv

import requests

from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

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

        date_column = row.find_all('td')[1]
        date_joined = date_column.span.text
        country_dict['Date Joined'] = date_joined

        countries.append(country_dict)

with open('data/countries.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=('Name', 'Date Joined'))
    writer.writeheader()
    writer.writerows(countries)
