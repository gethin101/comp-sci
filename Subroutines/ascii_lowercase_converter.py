letters = []
ascii_values = []
chosen = str(input("Enter a single lowercase word "))

length = len(chosen)

for x in range(length):
    letters.append(chosen[x])

print()
print(letters)

for x in range(len(letters)):
    ascii_values.append(ord(letters[x]))
   
for x in range(len(letters)):
    print(f"\nLetter: {letters[x]}")
    print(f"ASCII: {ascii_values[x]}")
