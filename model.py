import random

# Define suspects, weapons, and locations
suspects = ["Alice", "Bob", "Carol", "Eddie"]
weapons = ["Dagger", "Gun", "Rope", "Knife"]
locations = ["Store", "Library", "Theater", "Museum"]

def generate_solution(seed):
    random.seed(seed)
    # Shuffle suspects, weapons, and locations independently
    random.shuffle(suspects)
    random.shuffle(weapons)
    random.shuffle(locations)

    # Create the solution list with one combination for each suspect, weapon, and location
    solution = []
    for suspect, weapon, location in zip(suspects, weapons, locations):
        solution.append({"suspect": suspect, "weapon": weapon, "location": location, "isMurderer": False})

    # Randomly select one combination to be the murderer
    murderer_index = random.randint(0, len(solution) - 1)
    solution[murderer_index]["isMurderer"] = True  # Mark the random combination as the murderer
    return solution


# Get a Direct Hint: A hint that directly reveals a fact
def getDirectHint(solution):
    hint = {}
    category = random.choice(["suspect/location", "suspect/weapon", "weapon/location","suspect/location", "suspect/weapon", "weapon/location", "murderer"])

    if category == "suspect/location":
        selected = random.choice(solution)
        hint["text"] = selected['suspect'] + " was at the " + selected['location']+"."
        hint["details"] = (selected['suspect'],selected['location'])

    elif category == "suspect/weapon":
        selected = random.choice(solution)

        hint["text"] = selected['suspect']+" had the "+selected['weapon']+"."
        hint["details"] = (selected['suspect'],selected['weapon'])

    elif category == "weapon/location":
        selected = random.choice(solution)

        hint["text"] = "The "+selected['weapon'] + " was at the "+selected['location'] + "."
        hint["details"] = (selected['weapon'],selected['location'])

    elif category == "murderer":
        murdererClueType = random.randint(1, 3)  # Randomly choose one of the three murderer clues
        murderer = next(item for item in solution if item["isMurderer"])
        if murdererClueType == 1:
            hint["text"] = murderer['suspect'] + " was the murderer."
            hint["details"] = (murderer['suspect'],"was the murderer")
        elif murdererClueType == 2:

            hint["text"] = "The "+murderer['weapon'] + " was used by the murderer."
            hint["details"] = (murderer['weapon'],"was the murder weapon")
        elif murdererClueType == 3:
            hint["text"] = "The murder happened at the "+murderer['location'] + "."
            hint["details"] = (murderer['location'],"was the murder location")

    return hint


# Get an Indirect Hint: A hint that provides a clue without directly revealing the solution
def getIndirectHint(solution):
    hint = {}
    category = random.choice(["suspect/location", "suspect/weapon", "weapon/location", "suspect/location", "suspect/weapon", "weapon/location", "murderer"])

    if category == "suspect/location":
        suspect = random.choice(solution)
        possible_locations = list(set(item["location"] for item in solution) - {suspect["location"]})
        location = random.choice(possible_locations)
        hint["text"] = random.choice([
            suspect['suspect'] + " was NOT at the "+location +".",
            suspect['suspect'] + " has never been to the "+location +".",
            suspect['suspect'] + " was never near the "+location +".",
            suspect['suspect'] + " was somewhere other than the "+location +".",
            "Nobody saw "+suspect['suspect'] + " at the "+location +".",
            suspect['suspect'] + " was not anywhere close to the "+location +".",
            "There's no record of "+suspect['suspect'] + " being at the "+location +".",
            suspect['suspect'] + " was not involved in anything at the "+location +".",
            suspect['suspect'] + " has no connection to the "+location+".",
            "No one at the "+location+ " had seen "+suspect['suspect'] + ".",
            "Witnesses at the "+location+ " did not see "+suspect['suspect'] + ".",
            "People at the "+location+ " did not recognize "+suspect['suspect'] + ".",
            "Eyewitnesses at the "+location+ " did not notice "+suspect['suspect'] + ".",
            "Reports from the "+location+ " confirm "+suspect['suspect'] + " was not there.",
            "Security at the "+location+ " did not record "+suspect['suspect'] + ".",
            "There were no sightings of "+suspect['suspect'] + " at the "+ location +"."
        ])
        hint["details"] = (suspect['suspect'],"not "+location)

    elif category == "suspect/weapon":
        suspect = random.choice(solution)
        possible_weapons = list(set(item["weapon"] for item in solution) - {suspect["weapon"]} )
        weapon = random.choice(possible_weapons)
        hint["text"] = random.choice([
            suspect['suspect'] + " did NOT have the "+weapon+".",
            suspect['suspect'] + " does not own a "+weapon+".",
            suspect['suspect'] + " saw someone else with the "+weapon+".",
            suspect['suspect'] + " was not seen with the "+weapon+".",
            suspect['suspect'] + " never touched the "+weapon+".",
            suspect['suspect'] + " was not carrying the "+weapon+".",
            suspect['suspect'] + " was not the one holding the "+weapon+".",
            suspect['suspect'] + " had no reason to have the "+weapon+".",
            "The "+weapon+" does not belong to "+suspect['suspect'] + ".",
            "The "+weapon+" was not in "+suspect['suspect'] + "'s possession.",
            "The "+weapon+" was never with "+suspect['suspect'] + ".",
            "The "+weapon+" was not found with "+suspect['suspect'] + "."
        ])
        hint["details"] = (suspect['suspect'],"not "+weapon)

    elif category == "weapon/location":
        weapon = random.choice(solution)
        possible_locations = list(set(item["location"] for item in solution) - {weapon["location"]} )
        location = random.choice(possible_locations)
        hint["text"] = weapon['weapon'] + " was NOT found at the {location}."
        hint["details"] = (weapon['weapon'],"not "+location)

    elif category == "murderer":
        murdererClueType = random.randint(1, 3)
        notMurderer = random.choice([item for item in solution if item["isMurderer"] == False])
        if murdererClueType == 1:
            hint["text"] = notMurderer['suspect'] + " was NOT the murderer."
            hint["details"] = (notMurderer['suspect'],"not murderer")
        elif murdererClueType == 2:
            hint["text"] = "The murderer did NOT use the "+notMurderer['weapon'] + "."
            hint["details"] = (notMurderer['weapon'],"not murder weapon")
        elif murdererClueType == 3:
            hint["text"] = "The murder was NOT committed at the "+notMurderer['location'] + "."
            hint["details"] = (notMurderer['location'],"not murder location")

    return hint


def generate_hint(solution, hint_number):
    # print(hint_number, random.random())
    # print(random.random() < (1/15 * hint_number))
    if random.random() < 0.5:
        return getDirectHint(solution)
    else:
        return getIndirectHint(solution)

# Display the grid
def display_grid():
    print("\nLogic Grid Puzzle:")
    print("Suspects: {suspects}")
    print("Weapons: {weapons}")
    print("Locations: {locations}")
    print("\n")

# Main game loop
def play_game(seed):
    hints = []
    hint_number = 1

    print("Welcome to the Logic Grid Puzzle!\n")

    display_grid()
    solution = generate_solution(seed)
    while True:
        # prompt the user
        print("What would you like to do?\n  1. Get a hint\n  2. Solve the puzzle")
        userChoice = input()
        if userChoice == "1":
            nextHint = generate_hint(solution, hint_number)
            for i in range(50):
                if(nextHint["details"] not in hints):
                    break
                nextHint = generate_hint(solution, hint_number)
            hints.append(nextHint["details"])
            print("*"*hint_number)
            print("Hint #"+hint_number+": "+nextHint['text'] + "")
            print("*"*hint_number)
            hint_number += 1
        if userChoice == "2":
            finalGuess(solution)
            break


def finalGuess(solution):
    # Allow the player to guess the solution
    print("\nCan you solve the puzzle?")
    guess_suspect = input("Enter your guess for the suspect: ")
    guess_weapon = input("Enter your guess for the weapon: ")
    guess_location = input("Enter your guess for the location: ")

    # Find the solution with the murderer
    murderer = next((item for item in solution if item["isMurderer"]), None)

    if murderer and guess_suspect.lower() == murderer["suspect"].lower() and guess_weapon.lower() == murderer["weapon"].lower() and guess_location.lower() == murderer["location"].lower():
        print("\nCongratulations, you've solved the puzzle!")
    else:
        print("\nOops, that's not the correct solution.")
        print("The correct solution was: "+murderer['suspect'] + " with the "+murderer['weapon'] + " in the "+murderer['location'] + ".\n")

def main():
    seed = int(input("Enter a seed number for the puzzle: "))
    play_game(seed)

# Set up the game
# if __name__ == "__main__":
#     main()


# suspects = ["Alice", "Bob", "Charlie"]
# weapons = ["Dagger", "Gun", "Rope"]
# locations = ["Store", "Library", "Theater"]

# solution = [
#   {"suspect":"Alice", "weapon":"Dagger", "location":"Store","isMurderer":false},
#   {"suspect":"Bob", "weapon":"Gun", "location":"Library","isMurderer":false},
#   {"suspect":"Charlie", "weapon":"Rope", "location":"Theater","isMurderer":true}
# ]


