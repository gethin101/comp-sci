password = ""
valid = False

while valid == False:
    password = input("Enter lowercase 4 digit PIN: ")
    if len(password) == 4 and password[0] != chr(122):
        valid = True
        for char in password:
            if ord(char) < 97 or ord(char) > 122:
                valid = False
    else:
        print("Invalid Pin")
       
print(valid)
