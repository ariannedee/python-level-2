"""
Read a file with a number on each line. Print the sum of those numbers.
"""

sum_ = 0
with open('data/input.txt', 'r') as file:
    for line in file.readlines():
        sum_ += int(line)

print(sum_)
