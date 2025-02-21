import requests
from bs4 import BeautifulSoup

URL = 'https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations'

response = requests.get(URL)
response.raise_for_status()

html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')

countries = []

for row in table.find_all('tr'):
    a = row.th.a
    if a is None:
        continue

    link_content: str = a.string
    name = link_content.split(' (')[0]

    countries.append(name)

with open('countries.txt', 'w') as file:
    for country in countries:
        file.write(country + "\n")