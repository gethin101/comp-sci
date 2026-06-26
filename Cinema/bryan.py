
import numpy

enter_admin = True
PASSWORD = "admin"
admin = False
rows = 5
columns = 8
seating = numpy.full((rows,columns),"x")
film_lineup = {"Nemo":numpy.full((rows,columns),"x") ,
                "Star Wars": numpy.full((rows,columns),"x"),
                "Minecraft Movie": numpy.full((rows,columns),"x")
                 }
item_prices= {"popcorn": 2.80,
                 "slushy": 1.50,
                "haribos": 2.00}
#-------------------- PRINT SEATING PLAN -------------------------

#------------------------------------------------------------------------          
       

def main_system(mode,admin):

    global amount_owed
    amount_owed = 0
   
    #-------- Choose which mode to enter -------------

    if mode == "1":
        global enter_admin
        if enter_admin == True:
            for i in range(3):
                enter_password = input("Enter the admin password: ")
                if enter_password != PASSWORD:
                    print("Incorrect Password")
                    if i == 2:
                        print("You can no longer attempt to enter Admin Mode")
                     
                        enter_admin = False
                       
                    print(f"You have {2-i} tries left")
                else:
                    print("Access Granted")
                    admin = True
                    break
        else:
             print("You can no longer attempt to enter Admin Mode!")
    #------- Customer Mode -----------------------------
    elif mode == "2":
        print("You have entered Customer Mode")
        while True:
            choice = input("Would you like to select a seat(1), buy a food/drink(2) or pay for your purchases(3)? ")
            #---------- Choosing a Film --------------------
            if choice == "1":
                print("The current film lineup is:")#
                for i in film_lineup:
                    print("-" , i)
                which_film = input("Which film out of these would you like to watch? ")
                lists = ["A","B","C","D","E","F","G","H","I","J","K"]
                nums = []

                for i in range(columns):
                    nums.append(i+1)
                   
                def print_seat():
                    print(*nums)
                    i=0
                    for row in film_lineup[which_film]:
                        for element in row:
                            print(element, end=" ")
                        print(lists[i])
                        i+= 1        

                print_seat()
                while True:
                    print("All seats are £10!")
                    seat = input("What seat would you like: ")
                    print(ord(seat[0])-65)
                    if film_lineup[which_film][ord(seat[0])-65,int(seat[1])-1] == "-":
                        print("This seat is already taken!")
                        continue
                    film_lineup[which_film][ord(seat[0])-65,int(seat[1])-1] = "-"
                    print_seat()
                    print(f"Your seat has been booked for {which_film}!")
                    amount_owed += 10
                    choose_another = input("Do you want to choose another seat?(y/n) ")
                    if choose_another == "y":
                        continue
                    else:
                        break

            #----------------- Choosing Refreshments ---------------
            elif choice == "2":
                while True:
                    print("The current items being sold are:")
                    for i in item_prices:
                        print(f"{i} - {item_prices[i]:.2f}")
                    item_choice = input("Which item would you like to buy? ")
                    if item_choice not in item_prices:
                        print("This item is not for sale!")
                        continue
                    print(f"You have successfully purchased {item_choice}!")
                    amount_owed += item_prices[item_choice]
                    again = input("Would you like to buy another food/drink?(y/n) ")
                    if again == "y":
                        continue
                    else:
                        break
            elif choice == "3":
                print(f"£{amount_owed:.2f} is your total")
                print("Thanks for paying, enjoy your movie!")
                break
    print(admin)
    #--------------- Admin Mode ----------------------    
    while admin == True:
        check_items = input("Do you want to change the film lineup(1) or update prices(2)? ")
        #----------- Updating Films -----------------------
        if check_items == "1":
            print("The current film lineup is:" , ", ".join(film_lineup))
            add_or_remove = input("Would you like to add(1) or remove(2) a film? ")
            if add_or_remove == "1":
                add_film = input("Which film would you like to add? ")
                film_lineup[add_film] = numpy.full((rows,columns),"x")
            if add_or_remove == "2":
                remove_film = input("Which film would you like to remove? ")
                for i in range(len(film_lineup)-1):
                    if film_lineup[i].lower() == remove_film.lower():
                        film_lineup.remove(film_lineup[i])
            print("The current film lineup is now:", ", ".join(film_lineup))
        #-------------- Updating Prices --------------------
        elif check_items == "2":
            while True:
                print("The current items being sold are:")
                for i in item_prices:
                    print(f"{i} - {item_prices[i]:.2f}")
                which_item = input("Which item price would you like to update? ")
                price = input(f"What do you want to change {which_item} to? ")
                if which_item not in item_prices:
                    print("This item is not for sale!")
                    continue
                item_prices[which_item] = int(price)
                again = input("Would you like to update another items price?(y/n) ")
                if again == "y":
                    continue
                break
        break
   
while True:
    mode = input("Would you like to enter admin mode(1) or customer mode(2)? ")    
    main_system(mode,admin)
