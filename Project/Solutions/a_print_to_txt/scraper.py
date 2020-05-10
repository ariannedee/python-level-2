import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

# Todo: Update with your info
name = 'Arianne Dee'
email = 'ariannedee@gmail.com'
assert name and email

headers = {'User-Agent': f'{name} ({email})'}
response = requests.get(URL, headers=headers)
assert response.status_code == 200

html_doc = response.text

# Uncomment following lines if you have no internet or if the Wikipedia page has changed
# with open('../../UN_countries_full.html', 'r') as file:
#     html_doc = ''
#     for line in file:
#         html_doc += line

soup = BeautifulSoup(html_doc, 'html.parser')

with open('../UN_countries_full.html', 'w') as file:
    file.write(soup.prettify())

table = soup.find('table', attrs={'class': 'wikitable'})
assert table.caption.string

rows = table.tbody.find_all('tr')

country_list = []
for row in rows:
    country_name_th = row.find('th', attrs={'scope': 'row'})
    if country_name_th:
        country_name = country_name_th.a.string.strip()
        country_list.append(country_name)

assert len(country_list) > 100

with open('countries.txt', 'w') as file:
    for country in country_list:
        file.write(country + '\n')
