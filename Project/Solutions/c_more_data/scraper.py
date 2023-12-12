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
            'URL': name_link['href']
        }
        countries.append(country_dict)

print(countries)
print(len(countries))

for country in countries[0:3]:
    new_url = BASE_URL + country['URL']
    response = requests.get(new_url)

    try:
        response.raise_for_status()
    except Exception as e:
        print(f"Error getting request: {new_url}")
        print(repr(e))
        continue

    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    country['Latitude'] = soup.find('span', class_='latitude').string
    country['Longitude'] = soup.find('span', class_='longitude').string


with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=['Name', 'Date of admission', 'Latitude', 'Longitude', 'URL'])
    writer.writeheader()
    writer.writerows(countries)