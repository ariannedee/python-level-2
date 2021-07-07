import csv
import re
from time import sleep

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"

# Todo: Update with your info
name = "Arianne"
email = "arianne.dee.studios@gmail.com"
assert name and email

# Dictionary of HTTP headers
headers = {'User-Agent': f'{name} ({email})'}

response = requests.get(URL, headers=headers)
assert response.status_code == 200, f"Got response code {response.status_code}"

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find("table", class_="wikitable")
country_list = []
for row in table.find_all("tr"):
    if row.td:
        country_dict = {}
        td = row.find_all("td")[0]
        link = td.find_all("a")[1]
        country_name = link.string
        country_dict["Name"] = country_name
        country_dict['URL'] = BASE_URL + link['href']

        td = row.find_all("td")[1]
        date_joined = td.span.string
        country_dict["Date joined"] = date_joined

        country_list.append(country_dict)


def get_area(table):
    # Look up 'Regular expressions'
    # Some pages have an extra space after "Area", so trying to find an exact match will fail.
    # re.compile("Area") creates a pattern to look for
    tr = table.find('tr', string=re.compile("Area *")).next_sibling
    area = tr.td.text.strip()
    return area.split('[')[0].split('\xa0')[0]


def get_population(table):
    tr = table.find('tr', string="Population").next_sibling
    population = tr.td.text.strip()
    return population.split('[')[0].split(" ")[0]


errors = []
for country_dict in country_list[:4]:
    url = country_dict['URL']
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.table
    try:  # If any sub-page fails, skip it and keep track of it
        country_dict['Area'] = get_area(table)
        country_dict['Population'] = get_population(table)
    except AttributeError:
        errors.append(country_dict)
    sleep(1)  # Limit rate at which you request pages

if errors:  # Can investigate these pages further afterwards
    print(f'Error getting detail data from:')
    for country_dict in errors:
        print(f'  {country_dict["Name"]}: {country_dict["URL"]}')

with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=('Name', 'Date joined', 'Area', 'Population'), extrasaction='ignore')
    writer.writeheader()
    writer.writerows(country_list)
