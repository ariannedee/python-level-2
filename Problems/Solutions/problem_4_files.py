"""
A program that takes a letter and outputs a text file of
all of the countries that start with that letter
"""

countries = {}
with open('input.txt', 'r') as file:
    for line in file.readlines():
        starting_letter = line[0]
        country = line.strip()
        if starting_letter not in countries:
            countries[starting_letter] = []
        countries[starting_letter].append(country)

letter = input('Number of countries that start with letter: ')
letter = letter.capitalize()

print(len(countries[letter]))
