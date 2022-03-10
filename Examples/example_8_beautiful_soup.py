"""
Documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
"""
from bs4 import BeautifulSoup

with open('data/google.html', 'r') as file:
    html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')
buttons = soup.find_all('input', type='submit')
for button in buttons:
    print(button['value'])
