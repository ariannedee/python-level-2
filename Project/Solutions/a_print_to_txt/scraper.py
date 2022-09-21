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
country_names = []
for row in rows:
    name_col = row.find('th', scope='row')
    if name_col:
        link = name_col.a
        name = link.string
        country_names.append(name)

print(country_names)
with open('data/countries.txt', 'w') as file:
    for name in country_names:
        file.write(name)
        file.write('\n')
