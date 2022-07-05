import requests
from bs4 import BeautifulSoup
from csv import DictWriter

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

# Todo: Update with your info
name = None
email = None
assert name and email

# Dictionary of HTTP headers
headers = {'User-Agent': f'{name} ({email})'}
response = requests.get(URL, headers=headers)

assert response.status_code == 200, f"Got {response.status_code}: {response.reason}"

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')

country_dicts = []
rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    if len(cols) > 0:
        name_col = cols[0]
        name_str: str = name_col.text
        name = name_str.split('[')[0].strip()
        date_joined = cols[1].text.strip()
        country_dict = {
            'Name': name,
            'Date Joined': date_joined
        }
        country_dicts.append(country_dict)

print(country_dicts)

with open('data/countries.csv', 'w') as file:
    writer = DictWriter(file, fieldnames=['Name', 'Date Joined'])
    writer.writeheader()
    writer.writerows(country_dicts)
