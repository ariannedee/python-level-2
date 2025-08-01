"""
Translate a message from the user into a numeric code
"""

code = {
    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
    'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17,
    'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26
}

def encrypt(plaintext):
    ciphertext = ""
    for char in plaintext.lower():
        coded_char = code.get(char, char)
        ciphertext += str(coded_char) + ' '
    return ciphertext.strip()

assert encrypt("hello!") == "8 5 12 12 15 !", f"Got {encrypt('hello!')=}"

# Get a message from the user
message = input("What is your message? ")

print(encrypt(message))
