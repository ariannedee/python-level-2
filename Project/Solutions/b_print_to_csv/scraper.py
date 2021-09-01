import csv

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
        }
        countries_list.append(country_dict)

print(countries_list)

with open("data/countries.csv", "w") as file:
    writer = csv.DictWriter(file, ["Name", "Date joined"])
    writer.writeheader()
    writer.writerows(countries_list)
