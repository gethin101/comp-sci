def bubble_sort(arr):
    n = len(arr)
    for i in range (n):
        for j in range (0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

scores = []


no_scores = int(input("How many scores do you have? "))
for x in range(no_scores):
    score_input = int(input(f"\nEnter the score for {x+1}: "))
    scores.append(score_input)



bubble_sort(scores)
print(scores)
