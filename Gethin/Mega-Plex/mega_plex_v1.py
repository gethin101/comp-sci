from dataclasses import dataclass
import time

customerLoggedin = False
adminLoggedin = False
admin_login = ["admin","admin123"]

@dataclass
class Film:
    movie:str
    price:float
    category:str
    tickets:int

spiderman = Film("Spiderman", 9.99 , "Action", 60)
starwars = Film("Star Wars", 5.00 , "Science Fiction", 45)
LOTR = Film("Lord of the Rings", 6.50 , "Fantasy", 20)

films = [spiderman, starwars, LOTR]


login = str(input("Enter account username ")).lower()
if login in admin_login:
    password = str(input("Enter admin password    ")).lower()
    if password in admin_login:
        print()
        print("Admin logged in ")
        adminLoggedin = True
        time.sleep(1)
    else:
        print("Incorrect admin login ")
        time.sleep(1)
elif login not in admin_login:
    print()
    print(f"Customer logged in as {login}")
    customerLoggedin = True
    time.sleep(1)

if adminLoggedin:
    print()
    print("                     Current Movies: ")
    print("-----------------------------------------------------------------------")
    for film in films:
        print(f"- {film.movie} | £{film.price:.2f} | {film.category} | {film.tickets} tickets")
    print("-----------------------------------------------------------------------")
    print()

    admin_choice = str(input("Which movie would you like to change? ")).lower()
    edit_film = "none"
    for film in films:
        if film.movie.lower() == admin_choice:
            edit_film = film
            break
    if edit_film == "none":
        print("This isn't a movie you can edit ")







    
    
