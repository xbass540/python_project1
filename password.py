password = input('Enter a password')
result = {}# this is a dictionary not a list

if len(password) >=8:
    result["length"] = True
else:
    result["length"] = False

digit= False
for i in password:
    if i.isdigit():
        digit = True

result["digits"] = digit

uppercase = False

for i in password:
    if i.isupper():
        uppercase = True

result["uppercase"] = uppercase

print(result)

if all(result.values()):
    print("Strong Pass")
else:
    print("Weak password")