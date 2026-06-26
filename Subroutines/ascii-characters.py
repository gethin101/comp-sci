



program_choice = str(input("Enter 1 or 2 to pick a program  ")).lower()
if program_choice == "1":
    def character_script():
        character = input("\nEnter character: ")
        ascii = ord(character)
        print(f"The ASCII code is {ascii}")

    def ascii_script():
        ascii = int(input("\nEnter ASCII code: "))
        if ascii > 0 and ascii < 128:
            character = chr(ascii)
            print(f"The character is {character}")
        elif ascii < 0 or ascii > 127:
            print(f"Invalid ASCII code")



    print("=" * 27)
    print("Select an option: ")
    print("- Character to ASCII   (1)")
    print("- ASCII to Character   (2)")
    print("=" * 27)

    choice = str(input("Your choice:  "))

    if choice == "1":
        character_script()
    elif choice == "2":
        ascii_script()
    else:
        print("\nInvalid option")
        time.sleep(2)
        quit()
        

elif program_choice == "2":
    def encrypt_character(plain_char, shift_value):
        ascii = ord(plain_char) + shift_value
        new_character = chr(ascii)
        return new_character


    letter = str(input("Enter a single uppercase letter: "))
    shift = int(input("Enter a shift value: "))

    new_character = encrypt_character(letter, shift)
    print(f"Encrypted character is {new_character}")

    
