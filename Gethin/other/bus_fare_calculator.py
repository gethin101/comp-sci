under_16s = 0
over_16s = 0

under_16s_fare = 1.50
over_16s_fare = 2.50

def calculateGroupFare():
    global under_16s, over_16s, under_16s_fare, over_16s_fare
    for i in range(4):
        try:
            age = int(input("Enter age "))
            if age >= 16:
                over_16s += 1
            elif age < 16:
                under_16s += 1
        except:
            print("Enter a valid age! ")
    total_price = (under_16s * under_16s_fare) + (over_16s * over_16s_fare)
    discount_price = total_price * 0.9
    saved = total_price - discount_price

    print(f"\nThe bus fare is £{discount_price:.2f}")
    print(f"You have saved £{saved:.2f}")

while input("\nPress enter to run ") != -1:
    calculateGroupFare()
