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

assert response.status_code == 200, f"{response.status_code} - {response.reason}"

html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')

countries = []
rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    if len(cols) == 0:
        continue
    name_col = cols[0]
    links = name_col.find_all('a')
    flag_link = links[0]
    if flag_link.img:
        name_link = links[1]
    else:
        name_link = flag_link
    name = name_link.string
    countries.append(name)

print(countries)

with open('countries.txt', 'w') as file:
    for country in countries:
        file.write(country + '\n')
