import csv
import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"

name = None
email = None

assert name and email, "Fill in your name and email"

headers = {'User-Agent': f'{name} ({email})'}

response = requests.get(URL, headers=headers)
response.raise_for_status()

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

countries = []

table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')
for row in rows:
    name_column = row.th
    link = name_column.a
    if link:
        country_name = link.string
        date_of_admission = row.td.span.string
        country = {
            'Name': country_name,
            'Date of admission': date_of_admission,
        }
        countries.append(country)

print(countries[0])

with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=('Name', 'Date of admission'))
    writer.writeheader()
    writer.writerows(countries)
