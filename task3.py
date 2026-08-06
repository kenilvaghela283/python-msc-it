
password=input("enter your password:")
upper = lower = digit = special = False
repeat = False
spec_char="!@#$%^&*()-_=+[]{}|\\/:;'<>,.?"

for i in range(len(password)):
    ch = password[i]
    if ch.isupper():
        upper=True
    if ch.islower():
        lower=True
    if ch.isdigit():
        digit=True
    if ch in spec_char:
        special=True
    if i > 0 and password[i]==password[i-1]:
        repeat=True
        

if not upper:
    print("missing Uppercase")
if not lower:
    print("missing Lowercase")
if not digit:
    print("missing Digit")
if not special:
    print("missing special character")
if repeat:
    print("repeated consecutive character")

if upper and lower and digit and special and not repeat:
    print("password strong")
else:
    print("password weak")