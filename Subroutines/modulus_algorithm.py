num = int(input())
if not(num > 1) or not (num < 20):
    print("false")
elif(num > 1) and (num < 15):
    print("almost")
elif(num % 5) == 0:
    print("true")
else:
    print("unknown")
