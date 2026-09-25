
scores = []

for i in range(5):
    score = int(input("Enter a score: "))
    scores.append(score)

total = 0

for x in range(len(scores)):
    total += scores[x]
average = (total / 5)



highest = scores[0]
for g in range(len(scores)):
    if scores[g] > highest:
        highest = scores[g]



lowest = scores[0]
for h in range(len(scores)):
    if scores[h] < lowest:
        lowest = scores[h]

print(f"\nAverage score: {average}")
print(f"Highest score: {highest}")
print(f"Lowest score: {lowest}")
    
