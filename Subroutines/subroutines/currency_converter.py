#from pounds to euros

def get_pounds():
    GBP = float(input("Enter amount in £ "))
    return (GBP)

def convert_to_euro(amount_pounds):
    euro_rate = 1.15
    Euro = amount_pounds * euro_rate
    return Euro


amount_pounds = get_pounds()
print()
input()
amount_euros = convert_to_euro(amount_pounds)

print(f"£{amount_pounds:.2f} is the same as €{amount_euros:.2f}")
