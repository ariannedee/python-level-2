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

        td = row.find_all("td")[1]
        date_joined = td.span.string
        country_dict["Date joined"] = date_joined

        country_list.append(country_dict)

print(country_list)
print(len(country_list))

with open("data/countries.csv", "w") as file:
    writer = csv.DictWriter(file, ["Name", "Date joined"])
    writer.writeheader()
    writer.writerows(country_list)
