import requests
import shutil

URL = "https://upload.wikimedia.org/wikipedia/commons/a/aa/Requests_Python_Logo.png"
response = requests.get(URL, stream=True)
if response.status_code == 200:
    with open('data/requests.png', 'wb') as f:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, f)
