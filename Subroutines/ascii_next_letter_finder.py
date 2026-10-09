char1 = "A"
code1 = ord(char1)
print(f"{char1} : {code1}")

code2 = 70
char2 = chr(code2)
print(f"{code2} : {char2}")

char3 = "a"
code3 = ord(char3)
print(f"{char3} : {code3}")


letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
chosen = str(input("\nEnter a capital letter: "))

for x in range(len(letters)):
    if chosen == letters[x]:
        index = x

val_1 = chosen
val_2 = letters[index + 1]
val_3 = letters[index + 2]
val_4 = letters[index + 3]

print(f"\nValue 1: {val_1}")
print(f"Value 2: {val_2}")
print(f"Value 3: {val_3}")
print(f"Value 4: {val_4}")
