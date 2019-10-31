sum = 0
with open('input.txt', 'r') as file:
    for line in file.readlines():
        num = int(line)
        sum += num

print(f'Sum is {sum}')
