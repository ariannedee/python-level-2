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
    name_col = row.th
    name_link = name_col.a
    if name_link is None:  # Ignore header
        continue
    name = name_link.string
    countries.append(name)

print(countries)
print(len(countries))

with open('countries.txt', 'w') as file:
    file.write('\n'.join(countries))