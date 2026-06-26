#The Current Code:
def withdraw_cash(balance, amount):
    new_balance = balance - amount
    return new_balance

# Main logic
current_bal = 500

while True:
    print()
    print("====================================")
    request = int(input("How much would you like to withdraw? "))


    try:

        if request < 1 or request > 250:
            print("---------------------------------------------------")
            print("Enter a valid amount between £1 and £250")
            print("---------------------------------------------------")

            
        elif request > current_bal:
            print("---------------------------------------------------")
            print(f"You don't have enough money to withdraw £{request}")
            print("---------------------------------------------------")

        elif request > 1 and request < 250 and request < current_bal:
            current_bal = withdraw_cash(current_bal, request)
            print("------------------------------------")
            print(f"You have withdrawn £{request}")
            print("------------------------------------")


    except:
        print("---------------------------------------------------")
        print(f"You don't have enough money to withdraw £{request}")
        print("---------------------------------------------------")



    print(f"Current balance: £{current_bal}")


