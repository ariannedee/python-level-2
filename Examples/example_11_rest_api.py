"""
Get repository data from Github's REST API.
V3 REST API documentation: https://developer.github.com/v3/
To generate an authentication token for your user, follow: https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
"""

import json
import requests
import sys

BASE_URL = "https://api.github.com"  # The root of all of our api requests
URL = BASE_URL + '/user/repos'  # The specific data we want
headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Content-Type': 'application/json',
    'Authorization': 'token {Your token here}',  # See https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
}

# Make API request
response = requests.get(URL, headers=headers)

# Handle bad requests
if response.status_code != 200:
    print(response.status_code)
    print(response.text)
    sys.exit()

# Turn the response string into JSON data. Data is now a list of dictionaries representing repositories
data = json.loads(response.text)

# Now do what you want with the data
if len(data) > 0:
    # I want to list all of the attributes we can get from each repository
    print("Keys")
    for key in data[0].keys():
        print('  ' + key)

    # I also want to list each repository name
    print("\nRepository names")
    for repo in data:
        print('  ' + repo['full_name'])
