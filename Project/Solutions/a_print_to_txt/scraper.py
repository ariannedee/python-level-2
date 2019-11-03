import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

# Update with your info
name = None
email = None
assert name and email

headers = {'User-Agent': f'{name} ({email})'}
html_doc = requests.get(URL, headers=headers).text

# Uncomment following lines if you have no internet or if the Wikipedia page has changed
# with open('../../UN_countries_full.html', 'r') as file:
#     html_doc = ''
#     for line in file:
#         html_doc += line

soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', attrs={'class': 'wikitable'})

countries = []
for row in table.find_all('tr'):
    columns = row.find_all('td')
    if len(columns) > 0:
        country_name = columns[1].text.strip()
        country_name = country_name.split('[')[0]
        countries.append(country_name)

print(countries)

with open('countries.txt', 'w') as output:
    for country in countries:
        output.write(country + '\n')
