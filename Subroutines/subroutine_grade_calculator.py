#subroutine to calculate the average
error = False

def calc_average(total_points,count):
    if count == 0:
        return 0
    return total_points / count

#main
print("---- Grade Calculator ----")
num_tests = int(input("Enter number of tests: "))
print("---------------------------------")
total = 0

for i in range (num_tests):
    score = int(input(f"Enter score for test {i+1} (0-100):"))
    if score < 0 or score > 100:
        error = True
        continue
    total += score

final_avg = calc_average(total, num_tests)

if error:
    print()
    print("---------------------------------------")
    print(f"Error. {score} is not within the boundaries")
    print("---------------------------------------")

else:
    print()
    print("---------------------------------")
    print(f"Average score is {final_avg}")
    print("---------------------------------")
