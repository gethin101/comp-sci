import time
from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

customer_LoggedIn = False
admin_LoggedIn = False
login_attempt = 0
CINEMA_NAME = "Gethin-Plex"
total_price = 0

rows = ["A", "B", "C", "D", "E", "F"]
cols = range(1, 6)


admin_login = {
    "username": "admin",
    "password": "password"
}

user_login = {
    "username": "gethin",
    "password": "login",
    "wallet": 100.00
}



@dataclass
class Film:
    movie: str
    price: float
    category: str
    tickets: int

spiderman = Film("Spiderman", 7.00, "Action", 20)
starwars = Film("Star Wars", 4.99, "Science Fiction", 18)
jurassic_park = Film("Jurassic Park", 8.00, "Adventure", 15)

films = [spiderman, starwars, jurassic_park]


@dataclass
class Snack:
    snack: str
    price: float
    category: str

popcorn = Snack("Popcorn", 4.99, "Sweet")
hotdog = Snack("Hotdog", 2.99, "Savory")
nachos = Snack("Nachos", 3.00, "Savory")
drink = Snack("Drink", 2.50, "Drink")

snacks = [popcorn, hotdog, nachos, drink]

def display_snacks():
    print("\n     CURRENT SNACKS")
    print("-" * 50)
    for snack in snacks:
        print(f"- {snack.snack}")
        print(f"    Price    : £{snack.price:.2f}")
        print(f"    Category : {snack.category}")
        print("-" * 50)



#quits program
def rejection():
    print("\nEdit movie confirmation rejected")
    time.sleep(1)
    quit()

#prints all movies info out
def display_movies():
    print("\n     CURRENT MOVIES")
    print("-" * 50)
    for film in films:
        print(f"- {film.movie}")
        print(f"    Category : {film.category}")
        print(f"    Price    : £{film.price:.2f}")
        print(f"    Tickets  : {film.tickets}")
        print("-" * 50)


#----------------- Seat booking -----------------
def seat_booking(movie_name, seats_to_pick): 
    global rows, cols
    
    root = tk.Tk()
    root.title(f"{movie_name.title()} seat booking")

    #opens above everything else
    root.lift()
    root.attributes('-topmost', True)
    root.after(100, lambda: root.attributes('-topmost', False))

    picked = 0

    #runs everytime a seat is clicked
    def pick_seat(btn):
        nonlocal picked #(allows the function to change the variable)

        if btn["state"] == "disabled":
            return

        #turns the seat red & stops you from clicking it
        btn.config(bg="red", state="disabled", fg="white")
        picked += 1

        if picked == seats_to_pick:
            root.destroy()

    #makes the rows and columns from my variable at the start
    for r, row in enumerate(rows):
        for c, col in enumerate(cols):
            seat_id = f"{row}{col}"
            btn = tk.Button(root, text=seat_id, width=6, height=2, bg="#003366", fg="white",font=("Arial", 12, "bold"),disabledforeground="white")
            btn.grid(row=r, column=c, padx=5, pady=5)
            btn.config(command=lambda b=btn: pick_seat(b)) #runs function when clicked

    root.mainloop()


#------------ receipt ------------------
def print_receipt(customer_name, movie_name, amount, total_price):

    #library to get date & time
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y  %H:%M")

    print("\n" + "=" * 45)
    print(" " * 15 + f"{CINEMA_NAME} Receipt")
    print("=" * 45)
    print(f" Customer     : {customer_name.title()}")
    print(f" Movie           : {movie_name}")
    print(f" Tickets         : {amount}")
    print(f" Total Price   : £{total_price:.2f}")
    print(f" Balance        :£{user_login['wallet']:.2f}")
    print("-" * 45)
    print(f" Date & Time: {date_time}")
    print("-" * 45)
    print(" Thank you for booking with Gethin-Plex!")
    print("=" * 45)

  



#========= login ==========
def login():
    global admin_LoggedIn, customer_LoggedIn, login_attempt

    while True:  # keeps going until username is correct or runs out of attempts
        login_name = input("Enter username: ").lower()

        #----------------------- admin login ---------------------------
        if login_name == admin_login["username"]:
            print("-" * 66)
            confirm_admin = input("Are you sure you want to access ADMIN PANEL? (y/n) ").lower()
            print("-" * 66)

            if confirm_admin == "y":
                password = input("Enter password: ").lower()

                if password == admin_login["password"]:
                    admin_LoggedIn = True
                    print("\nLogged in as admin")
                    return

                else:
                    while login_attempt < 3:
                        login_attempt += 1
                        print(f"\nIncorrect password. Attempt {login_attempt}")
                        time.sleep(1)

                        if login_attempt < 3:
                            password = input("Enter password: ").lower()

                        if password == admin_login["password"]:
                            admin_LoggedIn = True
                            print("\nLogged in as admin")
                            return

                    print("\nToo many login attempts")
                    quit()

            else:
                print("\nAdmin login cancelled")
                quit()

        #-------------------- customer login ---------------------------
        elif login_name == user_login["username"]:
            confirm_login = input(f"Are you sure you want to login as {login_name.title()}? (y/n) ").lower()

            if confirm_login == "y":
                password = input("Enter password: ")

                if password == user_login["password"]:
                    customer_LoggedIn = True
                    print("\n" + "=" * 25)
                    print(f'Current balance: £{user_login["wallet"]:.2f}')
                    print("=" * 25)
                    time.sleep(2)
                    return

                else:
                    while login_attempt < 3:
                        login_attempt += 1
                        print(f"\nIncorrect password. Attempt {login_attempt}")
                        time.sleep(1)

                        if login_attempt < 3:
                            password = input("Enter password: ")

                        if password == user_login["password"]:
                            customer_LoggedIn = True
                            print("\nLogged in successfully")
                            return

                    print("\nToo many login attempts")
                    quit()

            else:
                print("\nCustomer login cancelled")
                quit()

        else:
            print("\nThis account doesn't exist. Try again.\n")
            time.sleep(1)


#intro animation (prints a line at a time)
box = [
"===============================================",
"|                                              |",                                                                                     
"|            WELCOME TO GETHIN PLEX            |",
"|                                              |",                                                                                                    
"==============================================="
]

for x in box:
    print(x)
    time.sleep(0.1)

print("-" * 15)
print("Accounts:")
print(f"- {admin_login['username'].title()}")
print(f"- {user_login['username'].title()}")
print("-" * 15)
print()

login()


#-------Customer logged in--------
def customer():
        global total_price
        print("-" * 82)
        print(f"Welcome to {CINEMA_NAME}, which movie would you like to see?")
        display_movies()

        selected_film = "None"
        while selected_film == "None":
            
            book_film = input("Enter movie: ").lower()

            for film in films:
                if film.movie.lower() == book_film:
                    selected_film = film
                    break

            if selected_film == "None":
                print("\nYou can't book this movie. Pick another from the list")
                time.sleep(2)
                display_movies()

        else:
            print(f"\nHow many tickets would you like to book for {selected_film.movie}?")

            try:
                amount = int(input("Number of tickets: "))
            except ValueError:
                print("\nError: This isn't a number of tickets")
                quit()

            if amount <= 0:
                print("\nYou have to buy at least 1 ticket")

            elif amount > selected_film.tickets:
                print(f"\nSorry, there are only {selected_film.tickets} tickets left")

            else:
                selected_film.tickets -= amount
                total_price += amount * selected_film.price
                print("=" * 50)
                print(f"Total price: £{total_price:.2f}")
                print("=" * 50)

                if user_login["wallet"] < total_price:
                    print("You don't have enough money in your wallet!")
                    print("-" * 60)
                    print(f"Your balance: £{user_login['wallet']:.2f}")
                    print(f"Total cost: £{total_price:.2f}")
                    print("-" * 50)
                    time.sleep(1)
                    print("Booking cancelled.")
                    time.sleep(2)
                    quit()

            
                time.sleep(1)
                seat_booking(selected_film.movie, amount)

                #snacks here
                snacks_buy = str(input("Would you like to purchase any snacks? (y / n) ")).lower()
                if snacks_buy == "y":
                    display_snacks()
                    time.sleep(1)
                    print("adding snacks soon... be patient!!")
                    time.sleep(3)


                    

        

                

                
                    

                
                time.sleep(1)
                print("-" * 85)
                user_login["wallet"] -= total_price
                print(f"Payment completed! Balance: £{user_login['wallet']:.2f}")
                print(f"You just booked {amount} tickets for {selected_film.movie}!   |   {selected_film.tickets} tickets left")
                print("-" * 85)

                time.sleep(2)
                print_receipt(user_login["username"], selected_film.movie, amount, total_price)


if customer_LoggedIn:
    customer()
            




#--------Admin logged in--------
elif admin_LoggedIn:
    display_movies()

    confirm_edit = input("Would you like to edit a movie? (y/n) ").lower()

    if confirm_edit == "n":
        rejection()

    elif confirm_edit == "y":
        edit_movie = input("Which movie would you like to edit? ").lower()
        selected_movie = "none"

        for film in films:
            if film.movie.lower() == edit_movie:
                selected_movie = film
                break

        if selected_movie == "none":
            rejection()

        section_edit = input(f"Which data would you like to edit for {selected_movie.movie}?   Price | Tickets | Category  ").lower()

        if section_edit == "price":
            print("-" * 53)
            selected_movie.price = float(input(f"Current price: £{selected_movie.price:.2f} | Enter new price: £"))
            print("-" * 53)
            print(f"{selected_movie.movie} price updated to £{selected_movie.price:.2f}!")
            print()
            time.sleep(1)
            display_movies()

    else:
        print('\nYou need to type "Y" or "N"')
        quit()
