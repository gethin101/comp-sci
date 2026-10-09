import time
import random
from datetime import datetime

print("=" * 15)
print("Reaction Time Test. ")
print("=" * 15)
time.sleep(1)

input("Press enter to start and again when told..  ")

time.sleep(random.uniform(1,6)) #(decimal)


print("\nPRESS ENTER ")
start = datetime.now()
input()
end = datetime.now()

reaction_time = (end - start).total_seconds()

time.sleep(0.5)

print(f"Your reaction time was {reaction_time:.3f}s ")

if reaction_time < 0.2:
    print("-" * 13)
    print("Incredible!")
    print("-" * 13)
elif reaction_time < 0.3:
    print("-" * 13)
    print("Very good!")
    print("-" * 13)
elif reaction_time < 0.4:
    print("-" * 13)
    print("Average")
    print("-" * 13)
else:
    print("-" * 13)
    print("Not bad")
    print("-" * 13)
