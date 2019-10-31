try:
    int('five')
    print('Success!')
except ValueError as e:
    print("Fail!")
    print(e)


print('Got here')

int('1.5')  # Run fails with exit code 1
print("Didn't get here")
