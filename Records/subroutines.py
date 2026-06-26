print("-------------------------- example 1 - Procedure (subroutine) ----------------------------")
#
#def means to define

def greet_user(name): # this has one parameter
    print(f"Hello {name}")


# to call subroutine :
# we call this four times so the subroutine runs four times
# the name in the brackets is being store in the variable name which is the parameter

greet_user("Gethin")
greet_user("James")
greet_user("Jan")
greet_user("Bryan")


print("-------------------------- example 2 - Function (subroutine) -----------------------------")

def Calc_square (number): # this has one parameter
    return number * number
    # the keyword return informs us that this is a function as it returns the value

print(Calc_square (4))
print(Calc_square (3))
print(Calc_square (2))
print(Calc_square (1))


print("---------- example 3 - local variables - only accessible inside the subroutine -----------")

def add_number(): # this has no parameters
    total = 10 + 5 # total is local variable because it's inside the subroutine
    print(total)

add_number() # the brackets are empty because it's not expecting an argument (data)


print("------------- example 4 - global variables - accessible throughtout program --------------")

player_score = 0

def add_points(points): # this has one parameter
    global player_score # need the word global to allow access to the varable

    # this subroutine is just going to add points
    player_score += points
    print(f"Points added to current score: {player_score}")

def display_score():
    # used to print the final score
    print (f"Final score is: {player_score}")

add_points(3)
add_points(41)
add_points(67)
display_score()
