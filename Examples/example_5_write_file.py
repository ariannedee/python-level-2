"""
Generate 100 random numbers. Write them to a file.
If the number is odd, end the line. The next number starts on a new line.
"""

import random

with open('data/output.txt', 'w') as file:
    for _ in range(100):
        number = random.randint(1, 100)
        file.write(str(number))  # Write number
        if number % 2 == 0:      # Number is even
            file.write(' ')      # Write a space
        else:                    # Number is odd
            file.write('\n')     # Write a new line
