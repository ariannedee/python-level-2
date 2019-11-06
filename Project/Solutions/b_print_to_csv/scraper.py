import csv

import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

# Todo: Update with your info
name = None
email = None
assert name and email

headers = {'User-Agent': f'{name} ({email})'}
html_doc = requests.get(URL, headers=headers).text
soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', attrs={'class': 'wikitable'})

countries = []
for row in table.find_all('tr'):
    columns = row.find_all('td')
    if len(columns) > 0:
        country_name = columns[1].text.strip()
        country_name = country_name.split('[')[0]
        country_data = {
            'Name': country_name,
            'Date Joined': columns[2].text.strip()
        }
        countries.append(country_data)

with open('countries.csv', 'w') as output:
    writer = csv.DictWriter(output, ['Name', 'Date Joined'])
    writer.writeheader()
    writer.writerows(countries)
