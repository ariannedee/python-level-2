import requests
from bs4 import BeautifulSoup
from csv import DictWriter

BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"

response = requests.get(URL)

response.raise_for_status()

html_doc = response.text

# with open('UN_countries_full.html', 'w', encoding="utf-8") as file:
#     file.write(html_doc)
#
# with open('UN_countries_full.html', 'r') as file:
#     html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')

countries = []
table = soup.find('table', class_='wikitable')
for row in table.find_all('tr'):
    col_1 = row.find('th', scope='row')
    if not col_1:
        continue
    name_link = col_1.a
    name = name_link.string
    date_joined = row.td.span.string
    country = {'name': name, 'date joined': date_joined, 'url': BASE_URL + name_link['href']}
    countries.append(country)

for country in countries[:3]:
    response = requests.get(country['url'])
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    lat = soup.find('span', class_='latitude').string
    lon = soup.find('span', class_='longitude').string
    country['latitude'] = lat
    country['longitude'] = lon

with open('data/countries.csv', 'w') as file:
    writer = DictWriter(file, fieldnames=['name', 'date joined', 'latitude', 'longitude'], extrasaction='ignore')
    writer.writeheader()
    writer.writerows(countries)
