"""
A program that takes a letter and outputs a text file of
all of the countries that start with that letter
"""
from collections import defaultdict

countries = defaultdict(list)
with open('data/countries.txt') as file:
    for country in file.readlines():
        first_letter = country[0].upper()
        countries[first_letter].append(country.strip())


# Get user to provide a letter
letter = input('Number of countries that start with letter: ')
letter = letter.capitalize()

letter_countries = countries[letter]

print(len(letter_countries))
print(letter_countries)

with open(f'data/{letter}_countries.txt', 'w') as file:
    for country in letter_countries:
        file.write(country + '\n')
