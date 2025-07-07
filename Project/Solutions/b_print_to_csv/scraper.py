import csv

import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

response = requests.get(URL)
response.raise_for_status()

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')

countries = []
for row in rows:
    name_col = row.th
    name_link = name_col.a
    if name_link is None:  # Ignore header
        continue
    name = name_link.string
    admission_date = row.td.span.string
    country = {'Name': name, 'Date of Admission': admission_date}
    countries.append(country)

print(countries)

with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, ['Name', 'Date of Admission'])
    writer.writeheader()
    writer.writerows(countries)