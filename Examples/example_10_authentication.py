import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://github.com/session"
USERNAME = "***"
PASSWORD = "***"

URL = "https://github.com"
headers = {'User-Agent': f'Your name (your@email.com)'}

# Create new session so that cookies are saved between requests
session_requests = requests.session()

# Get the authenticity token from the login page
login_page = session_requests.get(LOGIN_URL, headers=headers)
soup = BeautifulSoup(login_page.text, 'html.parser')

# The input name might be different depending on the site. Inspect the form and look for a hidden input with "authenticity" or "csrf".
authenticity_token = soup.find('input', attrs={'name': 'authenticity_token'}).get('value')
print(authenticity_token)

# Send login request
data = {
    'login': USERNAME,
    'password': PASSWORD,
    'authenticity_token': authenticity_token,
}
response = session_requests.post(LOGIN_URL, headers=headers, data=data)
print(response.status_code)

# Now you are authenticated and can start scraping the URL you want
response = session_requests.get(URL, headers=headers)

with open('data/logged_in.html', 'w') as file:  # Open this to verify that your login worked
    file.write(response.text)

# ... Do some scraping with the result
