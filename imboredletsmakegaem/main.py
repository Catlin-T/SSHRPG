import os
import time
import random
import sys


class Player(object):
    """Should be able to use this class for both
    enemies *and* the human player.

    """

    def __init__(self, name, attack, defense, agility,
                 luck, hitpoints, level=0, kills=0):

        """

        Args:
            name (str): --

        """

        self.name = name
        self.attack = attack
        self.defense = defense
        self.agility = agility
        self.luck = luck
        self.hitpoints = hitpoints
        self.level = level
        self.kills = 0

        self.max_hitpoints = hitpoints

    def assign_points(self, points):
        """Namely for HumanPlayer to distribute
        their stats into the hero.

        Args:
            points (int): Number of points to invest
                in stats.

        """

        stats = ["ATK", "DEF", "AGL", "LCK"]

        while points > 0:
            print "You have %s points remaining" % points
            print "Assign points by typing in the stat you want to boost.\n"
            print "ATK: %s" % self.attack
            print "DEF: %s" % self.defense
            print "AGL: %s" % self.agility
            print "LCK: %s \n" % self.luck
            selection = raw_input("$")

            if selection in stats:
                # Increase the selected stat by one
                setattr(self, selection, getattr(self, selection) + 1)
                points -= 1

            else:
                print "\nTry Again.\n"



# deprecated due to Player obj
def create_pc(name):
    character = {
        "Name": name,
        "ATK": 1,
        "DEF": 1,
        "AGL": 1,
        "LCK": 1,
        "Max HP": 10,
        "HP": 10,
        "LVL": 1,
        "Kills": 0
        }

    return character


def create_baddie(level):

    baddie = {
        "Name": "LVL. %s Goblin" % level,
        "ATK": random.randint(0,2 + level),
        "DEF": random.randint(0,2 + level),
        "AGL": random.randint(0,2 + level),
        "LCK": random.randint(0,2 + level),
        "HP": 5
        }
    
    return baddie


def print_stats(char):

    for stat, value in char.iteritems():
        print "%s: %s" % (stat, value)

    return None


def attack(attacker, defender):

    attack_roll = random.randint(0, attacker["LCK"]) + attacker["ATK"]
    defend_roll = random.randint(0, defender["LCK"]) + defender["DEF"]
    
    damage = attack_roll - defend_roll

    if damage < 0: damage = 0

    print "%s hit %s for %s damage!" % (attacker["Name"], defender["Name"], damage)
    
    return damage


def battle(player, baddy):

    agl_check = baddy["AGL"] > player["AGL"]

    if agl_check:
        print "Oh no! the enemy strikes first!"

    while True:
    
        if agl_check:
            print_stats(baddy)
            print "\nIt's this guy's turn.\n"
            raw_input("Enter to continue.")
            
            damage = attack(baddy, player)

            player["HP"] -= damage
            
            if player["HP"] <= 0: break
            
            print

            print_stats(player)
            print "\nIt's your turn.\n"
            raw_input("Enter to continue.")

            damage = attack(player, baddy)

            baddy["HP"] -= damage

            if baddy["HP"] <= 0: break
            
            print

        else:
            print_stats(player)
            print "\nIt's your turn.\n"
            raw_input("Enter to continue.")
            
            damage = attack(player, baddy)

            baddy["HP"] -= damage
            
            if baddy["HP"] <= 0: break
            
            print

            print_stats(baddy)
            print "\nIt's this guys turn.\n"
            raw_input("Enter to continue.")

            damage = attack(baddy, player)

            player["HP"] -= damage

            if player["HP"] <= 0: break
            
            print

    if player["HP"] <= 0: sys.exit("You died.")

    else:
        player["Kills"] += 1
        player["HP"] = player["Max HP"]

        if player["Kills"] == player["LVL"]:
            print "You leveled up!"
            assign_points(player, player["LVL"])
            player["LVL"] += 1
            player["Kills"] = 0

        return player


def main():

    os.system('clear' if os.name == 'posix' else 'cls')
    
    name = raw_input("What's your name? ")
    pl_char = create_pc(name)

    pl_char = assign_points(pl_char, 8)

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

    while True:

        enemy = create_baddie(random.randint(1, pl_char["LVL"] + 1))
        pl_char = battle(pl_char, enemy)

    return None

if __name__ == "__main__":
    main()
