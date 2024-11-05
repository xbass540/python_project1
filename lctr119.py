from converters import convert
from parser import parse

feet_inches=input("enter feet and inches")

parsed = parse(feet_inches)

result = convert(parsed['feet'], parsed['inches'])

print(f"{parsed['feet']} feet and {parsed['inches']} is equal to {result}")

if result < 1:
    print("is too small")
else:
    print("is OK")