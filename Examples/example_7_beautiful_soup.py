"""
Documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
"""
from bs4 import BeautifulSoup

with open('data/google.html', 'r') as file:
    html_doc = ''
    for line in file:
        html_doc += line

soup = BeautifulSoup(html_doc, 'html.parser')
buttons = soup.find_all('input', attrs={'type': 'submit'})
for button in buttons:
    print(button.get('value'))
