"""
Given a user's input of n, return a list of factorials from 0! to n!

Test cases:
0! = 1
1! = 1
2! = 1 x 2 = 2
4! = 1 x 2 x 3 x 4 = 24
"""


# Helper method to test equality
def assert_equals(actual, expected):
    assert actual == expected, f'Expected {expected}, got {actual}'


# Create a function that produces the factorial of a number
def factorial(n):
    total = 1
    for i in range(n):
        total *= (i + 1)
    return total


# Test factorial function
assert_equals(factorial(0), 1)
assert_equals(factorial(1), 1)
assert_equals(factorial(2), 2)
assert_equals(factorial(4), 24)


# Request a number from the user
number = int(input("Enter a positive whole number: "))


# Print a list of factorials from 0 to the given number
factorials = []
for i in range(number + 1):
    factorials.append(factorial(i))

print(factorials)
