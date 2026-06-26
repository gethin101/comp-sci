import time

customer_LoggedIn = False
admin_LoggedIn = False
login_attempt = 0

admin_login = ["admin","pass123"]

login = str(input("Enter username ")).lower()

if login == "admin":
    password = str(input("Enter password ")).lower()
    
    if password in admin_login:
        admin_LoggedIn = True
        print("\nLogged in as admin ")
    elif password not in admin_login:
        while login_attempt < 3:
            print("\n--------------------------------")
            login_attempt += 1
            print(f"Incorrect password.  Attempt: {login_attempt}")
            time.sleep(2)
            print("--------------------------------")

            if login_attempt < 3:
                password = str(input("\nEnter password ")).lower()

            if password in admin_login:
                print("\nLogged in as admin ")
                admin_LoggedIn = True
                break
    if login_attempt == 3:
        print("\nToo many login attempts ")
        
else:
    confirm_login = str(input(f"\nAre you sure you want to log in as {login}?  ( y / n ) "))
    if confirm_login == "y": 
        customer_LoggedIn = True
        print(f"\nCustomer logged in as {login}")
    elif confirm_login =="n":
        print("\nCustomer login rejected")
        time.sleep(1)
        quit()          
          


