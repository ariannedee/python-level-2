
with open('data/output.txt', 'w') as file:
    lines = ['a', 'b', 'c', 'd']
    file.writelines(lines)
    for line in lines:
        file.write(line + '\n')
