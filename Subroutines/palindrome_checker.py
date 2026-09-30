s = ""
while s != "x":
    s = str(input("\nEnter a word or phrase: "))
    max = (len(s) - 1)

    Matched = True

    for i in range(0, max + 1):
        Letter1 = s[i]
        Letter2 = s[max - i]

        if Letter1 != Letter2:
            Matched = False

    if Matched ==  True:
        print("Palindrome")
    else:
        print("Not a palindrome")
