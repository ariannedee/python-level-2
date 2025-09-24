from csv import DictWriter

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"

name = None
email = None

assert name and email, "Please supply your name and email"

headers = {"User-Agent": f"{name} ({email})"}
response = requests.get(URL, headers=headers)

response.raise_for_status()

html_doc = response.text

soup = BeautifulSoup(html_doc, "html.parser")

table = soup.find("table", class_="wikitable")

countries = []
for row in table.find_all("tr"):
    name_link = row.th.a
    if not name_link:
        continue
    name: str = name_link.string
    name = name.split(" (")[0]
    date_joined = row.td.span.string
    country_dict = {
        'Name': name,
        'Date joined': date_joined,
        'URL': name_link.get('href'),
    }
    countries.append(country_dict)

errors = []
for country in countries:
    response = requests.get(BASE_URL + country['URL'], headers=headers)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(repr(e))
        errors.append({
            "Country": country["Name"],
            "URL": BASE_URL + country["URL"],
            "Error": e,
        })
        continue
    html_doc = response.text

    soup = BeautifulSoup(html_doc, "html.parser")

    country['Latitude'] = soup.find("span", class_="latitude").string
    country['Longitude'] = soup.find("span", class_="longitude").string

with open("countries_more_data.csv", "w") as file:
    writer = DictWriter(file, fieldnames=("Name", "Date joined", "URL", "Latitude", "Longitude"))
    writer.writeheader()
    writer.writerows(countries)

with open("errors.csv", "w") as file:
    writer = DictWriter(file, fieldnames=("Country", "URL", "Error"))
    writer.writeheader()
    writer.writerows(countries)