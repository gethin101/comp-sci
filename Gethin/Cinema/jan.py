
# ---------------- VARIABLES ----------------

rows = 8
cols = 9

PASSWORD = "janiscool"
total_cost = 0

# ---------------- FUNCTIONS ----------------

def generate_seats():
    return [["X " for _ in range(cols)] for _ in range(rows)]

def display_seats(seats):
    print("\nSeating Plan:")
    for i in range(len(seats)):
        print(chr(65 + i), end=" ") # Print The A,B,Cs
        for j in range(len(seats[i])):
            print(seats[i][j], end=" ")# Print X/-
        print()

def choose_seat(seats, price):
    global total_cost
    choice = input("\nEnter seat (e.g. A1): ").upper()
   
    row = ord(choice[0:]) - 65
    col = int(choice[1:])

    if seats[row][col] == "X ":
        seats[row][col] = "- "
        print("Seat booked!")
        total_cost += price
    else:
        print("\n=====================================================")
        print("\nSeat already taken!")
        print("\n=====================================================")

def price_change():
    global films
    print("\nChange ticket price for which film?")
    print("\n=====================================================")
    print("")
    for i in range(len(films)):
        print(i, films[i]["name"], "£", films[i]["price"])
    print("\n=====================================================")
    change_number = int(input("Select film number: "))
    new_price = float(input("How much do you want to change it into? "))
    films[change_number]["price"] = new_price
    print(f"\nPrice changed successfully! Newest price for {films[change_number]['name']}: £{films[change_number]['price']:.2f}")

# ---------------- MAIN LOOP ----------------

films = [
    {"name": "Avengers", "price": 10, "seats": generate_seats()},
    {"name": "Batman", "price": 10, "seats": generate_seats()},
    {"name": "Dog Man", "price": 10, "seats": generate_seats()}
]

running = True

while running:
    print("\n=====================================================")
    print("\n=================Welcome to Mega-Plex================")
    print("\n=====================================================")
    print("\n[Mega-Plex Booking System]")
    print("\n-----------------------------------------------------")
    user = input("\nCustomer mode or Admin mode? (User/Admin) ").lower()

    if user == "user":
        while True:
            print("\nAvailable Films:")
            for i in range(len(films)):
                print(i+1, films[i]["name"], "£", films[i]["price"])

            film_choice = int(input("\nSelect a film by number: "))
            if film_choice > 3:
                print("\n=====================================================")
                print("\nPlease choose an availible movie!")
                print("\n=====================================================")
                continue

            selected_film = films[film_choice-1]
            seats = selected_film["seats"]
            movie_cost = selected_film["price"]

            print(f"\nYou selected: {selected_film['name']}")

            display_seats(seats)
            choose_seat(seats, movie_cost)

            again = input("\nBook another seat? (y/n): ").lower()
            if again != "y":

                points = int(input("\nHow many loyalty points do you have? "))

                discount = points / 100

                use = input("Do you want to use your points? (y/n): ").lower()

                if use == "y":
                    if discount > total_cost:
                        discount = total_cost

                    total_cost = total_cost - discount
                    print("\nDiscount applied!")

                print("\n=====================================================")
                print(f"\nYour total is £{total_cost:.2f}")
                print("\nThank you for using the cinema system!")
                print("\n=====================================================")
                break

    elif user == "admin":
        password_attempt = 0
        while password_attempt < 3:
            password_check = input("\nPlease enter the password to enter admin mode: ")

            if password_check != PASSWORD:
                print("\n=====================================================")
                print("\nIncorrect password")
                print("\n=====================================================")
                password_attempt += 1
            else:
                print("\nAccess given")
                print("\nSystem Shutdown [1] / Price Change [2]")
                print("\n=====================================================")
                print("")
                Admin_choice = input("What action would you like to take? ")
                if Admin_choice == "1":
                    quit()
                elif Admin_choice == "2":
                    price_change()
                break

        if password_attempt == 3:
            print("\nToo many attempts - returning to customer mode")
   
    else:
        print("Invalid option. Type User or Admin.")
