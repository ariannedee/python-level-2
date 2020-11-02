import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

# Todo: Update with your info
name = None
email = None
assert name and email

headers = {'User-Agent': f'{name} ({email})'}
response = requests.get(URL, headers=headers)
assert response.status_code == 200

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

countries = []

table = soup.find('table', attrs={"class": "wikitable"})
rows = table.find_all('tr')
for row in rows:
    if row.td:
        links = row.td.find_all('a')
        name = links[1].string
        countries.append(name)

assert len(countries) > 100

with open('countries.txt', 'w') as file:
    for country in countries:
        file.write(country)
        file.write('\n')
