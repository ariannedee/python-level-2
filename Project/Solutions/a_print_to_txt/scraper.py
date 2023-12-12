import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

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
        countries.append(name_link.string)

print(countries)
print(len(countries))

with open('countries.txt', 'w') as file:
    for country in countries:
        file.write(country + '\n')