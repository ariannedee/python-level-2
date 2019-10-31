"""
Return a list of factorials from 0! to n! given a user's input of n

E.g. 4! = 1 x 2 x 3 x 4 = 24
and 0! = 1
"""


# Create a function that produces the factorial of a number
def factorial(n):
    total = 1
    for i in range(n):
        total *= (i + 1)
    return total


# Request a number from the user
number = int(input("Enter a positive whole number: "))


# Print a list of factorials from 0 to the given number
factorials = []
for i in range(number):
    factorials.append(factorial(i))

print(factorials)
