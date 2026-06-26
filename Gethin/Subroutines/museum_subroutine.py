def museum(CountDays):
    count = 0
    for i in range(CountDays):
        visitors = int(input("How many visitors?"))
        if visitors > 200:
            count += 1
    return count

                
days_open = museum(int(input("How many days open in the last month?")))
                   
print(f"{days_open} days in the last month with >200 visitors")
