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


def factorial(num):
    product = 1
    for i in range(num):
        product *= i + 1
    return product

assert_equals(factorial(0), 1)
assert_equals(factorial(1), 1)
assert_equals(factorial(2), 2)
assert_equals(factorial(4), 24)

n = int(input("Enter an integer: "))

factorials = []
for i in range(n):
    factorials.append(factorial(i))

print(factorials)
