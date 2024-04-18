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
    if name_link:
        name = name_link.string
        countries.append(name)

with open('countries.txt', 'w') as file:
    for country in countries:
        file.write(country + '\n')
