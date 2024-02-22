import csv
import requests
from bs4 import BeautifulSoup

LOAD_DATA = False

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

if LOAD_DATA:
    response = requests.get(URL)
    print(response.status_code)
    response.raise_for_status()
    html_doc = response.text

    with open('wikipedia.html', 'w', encoding="utf-8") as file:
        file.write(html_doc)
else:
    with open('wikipedia.html', encoding="utf-8") as file:
        html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')
countries = []
for row in rows:
    name_col = row.th
    name_link = name_col.a
    if name_link is None:  # Header
        continue
    name = name_link.string
    date_of_admission = row.td.text.strip().split('[')[0]
    country = {
        'Name': name,
        'Date of admission': date_of_admission
    }
    countries.append(country)

with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, ('Name', 'Date of admission'))
    writer.writeheader()
    writer.writerows(countries)
