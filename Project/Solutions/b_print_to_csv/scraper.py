import csv

import requests
from bs4 import BeautifulSoup

URL = 'https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations'

response = requests.get(URL)
response.raise_for_status()

html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')

countries = []

for row in table.find_all('tr'):
    a = row.th.a
    if a is None:
        continue

    link_content: str = a.string
    name = link_content.split(' (')[0]
    date_joined = row.td.span.string

    country = {
        'Name': name,
        'Date joined': date_joined,
    }
    countries.append(country)

print(countries)

with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, ['Name', 'Date joined'])
    writer.writeheader()
    writer.writerows(countries)
