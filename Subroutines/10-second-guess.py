import time

input("Press enter to start and press again 10s later ")
start_time = time.time()
input()
end_time = time.time()

time_elapsed = (end_time - start_time)
print("=" * 20)
print(f"Time elapsed: {time_elapsed:.2f}s ")
print("=" * 20)

close = (10 - time_elapsed)
print(f"You were {close:.2f} seconds off ")
print("-" * 20)

if close < 0:
    print("Invalid ")
elif close <= 1:
    print("Result: Great job! ")
elif close < 2:
    print("Result: Decent job ")
elif close < 3:
    print("Result: Okay ")
else:
    print("Result: Awful ")
print("-" * 20)
