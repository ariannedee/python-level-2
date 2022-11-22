import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

# Todo: Update with your info
name = None
email = None
assert name and email

headers = {'User-Agent': f'{name} ({email})'}
response = requests.get(URL, headers=headers)

response.raise_for_status()

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')[1:]
countries = []
for row in rows:
    name = row.th.a.string
    countries.append(name)

print(len(countries))

with open("countries.txt", "w") as file:
    for country in countries:
        file.write(country)
        file.write('\n')
