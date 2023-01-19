import csv

import requests
from bs4 import BeautifulSoup
from requests import Response

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

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
    date_joined = row.td.span.string.strip()
    country: dict = {
        'Name': name,
        'Date joined': date_joined
    }
    countries.append(country)


with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, ['Name', 'Date joined'])
    writer.writeheader()
    writer.writerows(countries)
