import csv
import requests

from bs4 import BeautifulSoup
from time import sleep

BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"

# Todo: Update with your info
name = None
email = None
assert name and email

# Dictionary of HTTP headers
headers = {'User-Agent': f'{name} ({email})'}

response = requests.get(URL, headers=headers)

assert response.status_code == 200, f"{response.status_code} - {response.reason}"

html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')

table = soup.find('table', class_='wikitable')

countries = []
rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    if len(cols) == 0:
        continue
    name_col = cols[0]
    links = name_col.find_all('a')
    flag_link = links[0]
    if flag_link.img:
        name_link = links[1]
    else:
        name_link = flag_link
    name = name_link.string
    date_col = cols[1]
    date_joined = date_col.text.strip()
    country_dict = {
        "Name": name,
        "Date Joined": date_joined,
        "URL": name_link['href']
    }
    countries.append(country_dict)

for country in countries[:5]:
    print(f"Processing: {country['Name']}")
    url = BASE_URL + country['URL']
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        country["Latitude"] = 'Not found'
        country["Longitude"] = 'Not found'
        continue
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    country["Latitude"] = soup.find('span', class_='latitude').string
    country["Longitude"] = soup.find('span', class_='longitude').string
    sleep(0.5)

print(countries)

with open('countries.csv', 'w') as file:
    writer = csv.DictWriter(file, ["Name", "Date Joined", "Latitude", "Longitude"], extrasaction="ignore")
    writer.writeheader()
    writer.writerows(countries)
