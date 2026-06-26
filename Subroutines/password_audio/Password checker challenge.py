import time


password_length = False
numbers = False
character_check = False

from playsound import playsound
weak_audio = r'password_audio/weak_pass.mp3'
medium_audio = r'password_audio/medium_pass.mp3'
strong_audio = r'password_audio/strong_pass.mp3'
closing_program = r'password_audio/closing_program.mp3'
length_audio = r'password_audio/length_audio.mp3'
characters_audio = r'password_audio/characters_audio.mp3'
numbers_audio = r'password_audio/numbers_audio.mp3'
nothing_audio = r'password_audio/nothing_audio.mp3'


character_data = ["!","£","$","%","^","&","*","(",")","[","]",",",".","/","~","#"]
numbers_data = ["1","2","3","4","5","6","7","8","9","0"]
letters_data = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]


print()
password = str(input("Enter password to check strength..  "))



strength = 0
pass_strength = ""



#-------------- length -----------------

if len(password) >= 8:
    password_length = True
    strength += 1


elif len(password) < 8:
    password_length = False


#-------------- letters -----------------
    

if any(char in letters_data for char in password):
    letters = True
    strength += 1

elif not any(char in letters_data for char in password):
    letters = False


#------------- numbers -----------------
    

if any(char in numbers_data for char in password):
    numbers_check = True
    strength += 1

elif not any(char in numbers_data for char in password):
    numbers_check = False


#------------ characters ---------------


if any(char in character_data for char in password):
    character_check = True
    strength += 1

elif not any(char in character_data for char in password):
    character_check = False

#--------------------------------------



#def check_strength():

if strength == 4:
    pass_strength = "Strong"


elif strength == 3:
    pass_strength = "Medium"

else:
    pass_strength = "Weak"


#check_strength()
    

#---------------------------------------




print()
print(f"Strength: {strength}")
print()
print(f"Length check:    {password_length}")
print(f"Letters check:   {letters}")
print(f"Numbers check:   {numbers_check}")
print(f"Character check: {character_check}")
print()
print()

print(f"You password is: {pass_strength}")
print()
if pass_strength == "Weak":
    playsound(weak_audio)
elif pass_strength == "Medium":
    playsound(medium_audio)
elif pass_strength == "Strong":
    playsound(strong_audio)
    

print()



print("------------------------------")
print("Suggestions for improvement:")

if not password_length:
    print(f"- Add more length (min 8)")
    playsound(length_audio)

if not character_check:
    print(f"- Add more special characters")
    playsound(characters_audio)

if not numbers_check:
    print(f"- Add more numbers")
    playsound(numbers_audio)

elif numbers_check and character_check and password_length:
    print()
    print(f"Nothing - have a good day :)")
    playsound(nothing_audio)


#if not letters:
    #improvement_4 = "letters"
    #print(f"- Add more {improvement_4}")
print("------------------------------")



print()
time.sleep(1.5)
playsound(closing_program)
quit("Closing program... ")










