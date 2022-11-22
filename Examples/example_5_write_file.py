"""
Generate 100 random numbers. Write them to a file.
If the number is odd, end the line. The next number starts on a new line.
"""


with open('data/output.txt', 'w') as file:
    lines = ['a', 'b\n', 'c', 'd']
    for line in lines:
        file.write(line)
