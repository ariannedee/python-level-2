import csv

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"

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
    country = {
        'Name': name,
        'Date of Admission': admission_date,
        'URL': name_link['href']
    }
    countries.append(country)

errors = []
for country in countries:
    url = BASE_URL + country['URL']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        country['Latitude'] = soup.find('span', class_='latitude').string
        country['Longitude'] = soup.find('span', class_='longitude').string
    except Exception as e:
        error = {
            'Country': country['Name'],
            'URL': url,
            'Error': repr(e),
        }
        errors.append(error)

print(errors)
with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, ['Name', 'Date of Admission', 'Latitude', 'Longitude', 'URL'])
    writer.writeheader()
    writer.writerows(countries)

with open('errors.csv', 'w') as file:
    writer = csv.DictWriter(file, ['Country', 'URL', 'Error'])
    writer.writeheader()
    writer.writerows(errors)