"""
Documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
"""
from bs4 import BeautifulSoup

with open('data/sample.html', 'r') as file:
    html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')


# Print the HTML document with nesting and indentation
print(soup.prettify(formatter='html'))


# FINDING MULTIPLE ELEMENTS

soup.find_all('a')                             # Find all elements (returns a list)
soup.find_all('a', attrs={'class': 'sister'})  # Filter with attributes dict
soup.find_all('a', class_='sister')            # Filter with keyword arguments
soup.find_all('a', string='Elsie')             # Filter by content


# FINDING A SINGLE ELEMENT

soup.a                                 # Get the first child element
soup.find('a', attrs={'id': 'link1'})  # Filter with attributes dict
soup.find('a', id='link1')             # Filter with keyword arguments
soup.find('a', string='Elsie')         # Filter by content


# GETTING DATA FROM AN ELEMENT
link = soup.a

link.string       # Get text of an element (no nested content)
link.text         # Get text of an element (including nested content)
link['href']      # Get attribute of an element (if it exists)
link.get('href')  # Get attribute (if it might not exist)
