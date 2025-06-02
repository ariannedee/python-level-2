import requests

URL = "https://google.com"

# Dictionary of HTTP headers
headers = {'User-Agent': f'your@email.com'}  # Metadata for request
params = {'param1': 123, 'param2': 456}      # Adds ?param1=123&param2=456 to URL

response = requests.get(URL, params=params, headers=headers)

# Full list of HTTP status codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
# Common status codes:
# - 200 OK
# - 401 Unauthorized
# - 404 Not found
# - 502 Bad gateway
print(response.status_code)
print(response.reason)

# Raise exception if unsuccessful
response.raise_for_status()

# Get text contents
print(response.text)

with open('data/google.html', 'w', encoding="utf-8") as file:
    file.write(response.text)
