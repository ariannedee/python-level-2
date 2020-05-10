import csv
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"

# Todo: Update with your info
name = None
email = None
assert name and email

headers = {'User-Agent': f'{name} ({email})'}
response = requests.get(URL, headers=headers)
assert response.status_code == 200

html_doc = response.text

# Uncomment following lines if you have no internet or if the Wikipedia page has changed
# with open('../../UN_countries_full.html', 'r') as file:
#     html_doc = ''
#     for line in file:
#         html_doc += line

soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', attrs={'class': 'wikitable'})
assert table.caption.string

rows = table.tbody.find_all('tr')

country_list = []
for row in rows:
    country_name_th = row.find('th', attrs={'scope': 'row'})
    if country_name_th:
        country_name = country_name_th.a.string.strip()
        country_url = country_name_th.a['href']
        date_joined_td = row.find_all('td')[1]
        date_joined = date_joined_td.span.string.strip()

        country_data = {
            'Name': country_name,
            'Date Joined': date_joined,
            'URL': BASE_URL + country_url
        }

        country_list.append(country_data)

assert len(country_list) > 100


def get_population(table):
    tr = table.find('tr', attrs={'class': 'mergedtoprow'}, string='Population')
    text = tr.next_sibling.find('td').text
    return text.strip().split('[')[0].strip()


def get_area(table):
    tr = table.find('tr', attrs={'class': 'mergedtoprow'}, string='Area ')
    if not tr:
        tr = table.find('tr', attrs={'class': 'mergedtoprow'}, string='Area')

    text = tr.next_sibling.find('td').text
    return text.split('\xa0')[0].split('[')[0].strip()


for country_dict in country_list[:3]:
    response = requests.get(country_dict['URL'], headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('table', attrs={'class': 'geography'})
    assert len(tables) == 1

    table = tables[0]
    country_dict['Area (km2)'] = get_area(table)
    country_dict['Population'] = get_population(table)

    time.sleep(0.5)

with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, ('Name', 'Date Joined', 'Area (km2)', 'Population'), extrasaction='ignore')
    writer.writeheader()
    writer.writerows(country_list)
