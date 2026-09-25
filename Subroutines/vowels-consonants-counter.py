
word = str(input("Enter a single word: "))
vowels = 0
consonants = 0

for letter in word.lower():
    if letter in "aeiou":
        vowels +=1

consonants = (len(word)-vowels)

count_a = 0
count_e = 0
count_i = 0
count_o = 0
count_u = 0

for letter in word.lower():
    if letter == "a":
        count_a += 1
for letter in word.lower():
    if letter == "e":
        count_e += 1
for letter in word.lower():
    if letter == "i":
        count_i += 1
for letter in word.lower():
    if letter == "o":
        count_o += 1
for letter in word.lower():
    if letter == "u":
        count_u += 1

if vowels == 0:
    most_common = "N/A"
else:
    highest = max(count_a, count_e, count_i, count_o, count_u)

    if highest == count_a:
        most_common = "a"
    elif highest == count_e:
        most_common = "e"
    elif highest == count_i:
        most_common = "i"
    elif highest == count_o:
        most_common = "o"
    else:
        most_common = "u"
    
 


print(f"\nVowels in {word}: {vowels} ")
print(f"Consonants in {word}: {consonants}")
print(f"Most common vowel: {most_common}")
        
