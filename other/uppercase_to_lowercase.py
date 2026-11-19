word = input()
print(f"Original word: {word}")
new_word = ""

for i in range(len(word)):
    if ord(word[i]) < 65 or ord(word[i]) > 90:
        new_word += word[i]
    else:
        new_word += chr(ord(word[i]) + 32)

print(f"New word: {new_word}")
