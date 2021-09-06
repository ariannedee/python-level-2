import csv
import re

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

assert response.status_code == 200, f"Status was {response.status_code}"

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

countries_list = []
table = soup.find("table", class_="wikitable sortable")
for row in table.find_all("tr"):
    cols = row.find_all("td")
    if cols:
        name_col = cols[0]
        links = name_col.find_all("a")
        name = links[1].string
        date_joined = cols[1].span.string
        country_dict = {
            "Name": name,
            "Date joined": date_joined,
            "URL": links[1]["href"],
        }
        countries_list.append(country_dict)


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


errors = {}
for country_dict in countries_list[:3]:
    url = BASE_URL + country_dict["URL"]
    response = requests.get(url, headers=headers)

    assert response.status_code == 200, f"Status for {url} was {response.status_code}"

    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.find_all("table", class_="geography")[0]
    try:  # If any sub-page fails, skip it and keep track of it
        country_dict['Area'] = get_area(table)
        country_dict['Population'] = get_population(table)
    except AttributeError as e:
        errors[country_dict["Name"]] = e

if errors:  # Can investigate these pages further afterwards
    print(f'Error getting detail data from:')
    for name, error in errors.items():
        print(f'  {name}: {error}')

with open("data/countries.csv", "w") as file:
    writer = csv.DictWriter(file, fieldnames=('Name', 'Date joined', 'Area', 'Population'), extrasaction='ignore')
    writer.writeheader()
    writer.writerows(countries_list)
