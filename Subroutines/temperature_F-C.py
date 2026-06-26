run = True


def celcius_to_fahrenheit(c):
    return  (c * 9/5) + 32



def fahrenheit_to_celcius(f):
    return  (f - 32) * 5/9


while run:
    print()
    define_type = input("Which type is your temperature in?   ( F  /  C )   ").upper()

    if define_type not in ("F", "C"):
        print("Error. Enter your temperature type.  ")
        print()
        continue

    if define_type == "F":
        type_1 = "fahrenheit"
        type_2 = "celcius"

    else:
        type_1 = "celcius"
        type_2 = "fahrenheit"
        
    print()
    define_int = float(input(f"Enter your number in {type_1}  "))


    
    if define_int <= -273 and define_type == "C":
        print("Error. Enter a value larger than absolute zero.  ")
        continue

    if define_int <= -459 and define_type == "F":
        print("Error. Enter a value larger than absolute zero.  ")
        continue


    if define_type == "C":
        converted_temp = celcius_to_fahrenheit(define_int)
    else:
        converted_temp = fahrenheit_to_celcius(define_int)

    print()
    print("==============================================")
    print(f"Your original temperature in {type_1} -->  {define_int}")
    print(f"Your converted temperature in {type_2} -->  {converted_temp}")
    print("==============================================")
    print()

    
        
