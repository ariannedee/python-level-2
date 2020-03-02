"""
Get repository data from Github's GraphQL API.
V4 GraphQL API documentation: https://developer.github.com/v4/
To generate an authentication token for your user, follow: https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
"""

import json
import requests
import sys

API_URL = "https://api.github.com/graphql"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'token {Your token here}',  # See https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
}

# Specify the data you want from the API, test at https://developer.github.com/v4/explorer
query = """
query {
  viewer {
    repositories(first:100) {
      totalCount
      nodes {
        nameWithOwner
      }
    }
  }
}
"""
# Send the query in the right format for GraphQL
data = json.dumps({"query": query})
response = requests.post(API_URL, headers=headers, data=data)

# Handle bad requests (e.g. not authenticated)
if response.status_code != 200:
    print(response.status_code)
    print(response.text)
    sys.exit()

# Turn the response string into JSON data. Data is now a list of dictionaries representing repositories
response = json.loads(response.text)

# Handle bad queries (e.g. improperly formatted query string)
if 'errors' in response:
    print(response['errors'])
    sys.exit()

data = response['data']
print(data)

# Now do what you want with the data
repos = data['viewer']['repositories']['nodes']
if len(repos) > 0:
    # I want to list each repository name
    print("\nRepository names")
    for repo in repos:
        print('  ' + repo['nameWithOwner'])
