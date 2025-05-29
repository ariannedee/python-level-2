import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

response = requests.get(URL)
response.raise_for_status()
html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')

countries = []

for row in rows:
    name_link = row.th.a
    if not name_link:
        continue

    name: str = name_link.string
    countries.append(name.split(' (')[0])

with open('countries.txt', 'w') as file:
    file.write('\n'.join(countries))