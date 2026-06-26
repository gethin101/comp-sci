#subroutine to calculate the tax

def calculateTax(price): #1 parameter
    taxAmount = price * 0.2 #calculating tax amount
    #arithmetic operator is multiply *
    return taxAmount

#subroutine to calculate the final bill
def finalBill(original_price, taxAmount): #2 paramaters
    total = original_price + taxAmount
    return ("Total: £ " + str(total))

#main program
itemCost = 50
VAT = calculateTax(itemCost) #pass 50 into subroutine calculateTax - returns 10
receipt = finalBill(itemCost, VAT) #passes 50 and 10
print(receipt) #Prints: Total: £60  (returns float as multiplying by decimal)
