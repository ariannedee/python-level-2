import csv
import requests

from bs4 import BeautifulSoup

LOAD_DATA = False
URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

if LOAD_DATA:
    response = requests.get(URL)
    response.raise_for_status()
    html_doc = response.text

    with open('countries.html', 'w', encoding="utf-8") as file:
        file.write(html_doc)
else:
    with open('countries.html', encoding="utf-8") as file:
        html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')

countries = []
for row in rows:
    th = row.th
    name_link = th.a
    if not name_link:  # header row
        continue
    name = name_link.string
    date_admitted = row.td.span.string
    country = {
        'Name': name,
        'Date admitted': date_admitted,
    }
    countries.append(country)

print(countries)
with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=('Name', 'Date admitted'))
    writer.writeheader()
    writer.writerows(countries)
