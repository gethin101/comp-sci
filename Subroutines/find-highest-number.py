
numbers = []

for x in range(5):
    entered = int(input("Enter a number: "))
    numbers.append(entered)


highest = numbers[0]

for i in range(len(numbers)):
    if numbers[i] > highest:
        highest = numbers[i]

print(f"\nHighest number is {highest} ")
print(numbers)
