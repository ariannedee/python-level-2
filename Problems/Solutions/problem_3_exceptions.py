"""
Given a temperature (in Celsius), print the state of water at that temperature
"""

while True:
    try:
        temp = float(input("What's the temperature? "))
        break
    except ValueError:
        print("Try again! It must be a number")

if temp <= 0:
    print("  It’s freezing")
elif temp >= 100:
    print("  It’s boiling")
else:
    print("  It's alright")
