import random
randomNumber = random.randrange(1,101)
print("Enter a number")
userNumber = int(input())
while userNumber < 1 or userNumber > 100:
    print("Invalid number")
    userNumber = int(input())
print("Valid number entered")
if randomNumber == userNumber:
    print("Number guessed correctly")
