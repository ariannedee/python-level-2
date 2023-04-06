import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

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
    countries.append(name)

with open('data/countries.txt', 'w') as file:
    for country in countries:
        file.write(country)
        file.write('\n')
