import os
import time
import random


def create_pc(name):

    character = {
        "Name": name,
        "ATK": 1,
        "DEF": 1,
        "AGL": 1,
        "LCK": 1,
        "Max HP": 10,
        "HP": 10,
        "Weapon": None
        }

    return character

def create_baddie():

    baddie = {
        "Name": "Goblin",
        "ATK": random.randint(0,3),
        "DEF": random.randint(0,3),
        "AGL": random.randint(0,3),
        "LCK": random.randint(0,3),
        "HP": 5
        }

def main():

    os.system('clear' if os.name == 'posix' else 'cls')
    
    name = raw_input("What's your name? ")
    pl_char = create_pc(name)

    print "*BOOM*"

    time.sleep(2)

    print "*BOOM BOOM*"

    time.sleep(2)

    print "HEY! Get up! We're under attack!"
    print "Get your ass up, pick up a weapon, and defend the village!"

    time.sleep(1)

    print "..."

    time.sleep(1)

    print "Welp, no weapons. Looks like our feline god named 'Lin' has forsaken you."
    print "Now go fight."


    
    return None

if __name__ == "__main__":
    main()
