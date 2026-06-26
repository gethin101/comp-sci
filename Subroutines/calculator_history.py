
run = True

history = []

def calculate(num1, num2, op):
    if op == "*":
        return num1 * num2
    if op == "/":
        return num1 / num2
    if op == "+":
        return num1 + num2
    if op == "-":
        return num1 - num2


while run:
    print()
    num1 = float(input("Enter first number:  "))
    op = str(input("Select your arithmetic operator:   (+  -  /  *)   "))
    num2 = float(input("Enter second number:  "))


    result = calculate(num1, num2, op)

    history.append(result)
    if len(history) > 3:
        history.pop(0)


    print()
    print("==================================")
    print(f"Result: {num1} {op} {num2} =  {result}")
    print("==================================")

    print()
    print("--------------------------")
    print("Last 3 results:")

    for item in history:
        print(" -", item)

    print("--------------------------")
    print()

    


    


    
