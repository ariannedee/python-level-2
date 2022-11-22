import csv
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
country_dicts = []
for row in rows:
    name = row.th.a.string
    date_joined = row.td.span.string
    country_dict = {'Name': name, 'Date Joined': date_joined}
    country_dicts.append(country_dict)

print(country_dicts)

with open("countries.csv", "w") as file:
    writer = csv.DictWriter(file, fieldnames=['Name', 'Date Joined'])
    writer.writeheader()
    writer.writerows(country_dicts)
