from dataclasses import dataclass
@dataclass

class Character:
    name:str
    health:float
    inv_full:bool


gethin = Character("Master Gethin", 20.00, False)
james = Character("James", 5.5, True)


if gethin.inv_full == True:
    gethin_full = "Full"

if gethin.inv_full == False:
    gethin_full = "Not full"

if james.inv_full == True:
    james_full = "Full"

if james.inv_full == False:
    james_full = "Not full"


def print_info():

    gethin_full = "Full" if gethin.inv_full else "Not full"
    james_full = "Full" if james.inv_full else "Not full"
    
    print()
    print("=============Players=============")
    print("----------------------------------")
    print("            Character 1             ")
    print()
    print(f"Name ----> {gethin.name}")
    print(f"Health ----> {gethin.health} hearts")
    print(f"Inventory ----> {gethin_full}")
    print()
    print("----------------------------------")
    print("            Character 2             ")
    print()
    print(f"Name ----> {james.name}")
    print(f"Health ----> {james.health} hearts")
    print(f"Inventory ----> {james_full}")
    print()
    print("==================================")



def change_health():
    gethin.health = float(input(f"What health is {gethin.name} on now? "))
    james.health = float(input(f"What health is {james.name} on now? "))

print_info()
change_health()

for x in range(50):
    print()

print_info()

