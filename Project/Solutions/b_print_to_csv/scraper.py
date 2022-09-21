import csv
import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"
DOWNLOAD = False

# Todo: Update with your info
name = None
email = None
assert name and email
headers = {'User-Agent': f'{name} ({email})'}

if DOWNLOAD:
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    html_doc = response.text
    with open('data/wikipedia.html', 'w', encoding="utf-8") as file:
        file.write(response.text)
else:
    with open('data/wikipedia.html', 'r', encoding="utf-8") as file:
        html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')
table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')
countries = []
for row in rows:
    name_col = row.find('th', scope='row')
    if name_col:
        link = name_col.a
        name = link.string
        date_joined = row.td.text.strip()
        country = {
            'Name': name,
            'Date Joined': date_joined,
        }
        countries.append(country)

with open('data/countries.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=('Name', 'Date Joined'))
    writer.writeheader()
    writer.writerows(countries)
