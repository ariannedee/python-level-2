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

table = soup.find('table', attrs={'class': 'wikitable'})

countries = []
for row in table.find_all('tr'):
    tds = row.find_all('td')
    if len(tds) == 0:
        continue
    name_link = tds[0].a
    name = name_link['title']
    countries.append(name)

with open('data/countries.txt', 'w') as file:
    for country in countries:
        file.write(country)
        file.write('\n')
