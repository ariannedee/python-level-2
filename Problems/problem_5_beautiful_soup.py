"""
Print the text of the two buttons on the Google homepage.

Documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
"""
from bs4 import BeautifulSoup

with open('data/google.html', 'r') as file:
    html_doc = file.read()

print(html_doc)
