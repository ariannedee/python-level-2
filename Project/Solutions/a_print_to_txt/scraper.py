import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

# Todo: Update with your info
name = None
email = None
assert name and email

# Dictionary of HTTP headers
headers = {'User-Agent': f'{name} ({email})'}
response = requests.get(URL, headers=headers)

response.raise_for_status()

html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')

countries = []

table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    if not cols:
        continue
    name_col = cols[0]
    name = name_col.a['title']
    countries.append(name)

with open('data/countries.txt', 'w') as file:
    for country in countries:
        file.write(country)
        file.write('\n')
