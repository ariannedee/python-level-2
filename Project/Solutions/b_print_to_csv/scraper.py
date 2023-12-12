import csv

import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

response = requests.get(URL)

response.raise_for_status()

html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')

countries = []

rows = table.find_all('tr')
for row in rows:
    name_link = row.th.a
    if name_link is not None:
        name = name_link.string
        date = row.td.span.string
        country_dict = {
            'Name': name,
            'Date of admission': date,
        }
        countries.append(country_dict)

print(countries)
print(len(countries))

with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=['Name', 'Date of admission'])
    writer.writeheader()
    writer.writerows(countries)