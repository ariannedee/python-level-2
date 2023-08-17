import csv
import requests
from bs4 import BeautifulSoup


GET_DATA = False
WRITE_DATA = True

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

name = None
email = None
headers = {'User-Agent': f'{name} ({email})'}

if GET_DATA:
    response = requests.get(URL, headers=headers)

    response.raise_for_status()

    with open('wikipedia.html', 'w', encoding="utf-8") as file:
        html_doc = response.text
        file.write(html_doc)
else:
    with open('wikipedia.html', 'r') as file:
        html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')
table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')

countries = []
for row in rows:
    name_link = row.th.a
    if not name_link:  # Header row
        continue

    name = name_link.string
    date = row.td.span.string
    country = {
        'Name': name,
        'Date Joined': date,
    }
    countries.append(country)

if WRITE_DATA:
    with open('countries.csv', 'w') as file:
        writer = csv.DictWriter(file, ['Name', 'Date Joined'])
        writer.writeheader()
        writer.writerows(countries)
