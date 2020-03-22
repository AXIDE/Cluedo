import random
import json
import requests
import datetime
import github3
import schedule

class Game_Consts:
    ##Constructor references for the global lists and variables.
    suspects = ["Green", "Mustard", "Peacock", "Plum", "Scarlett", "White"]
    weapons = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
    rooms = ["Ballroom", "Billiard Room", "Conservatory", "Dining Room", "Hall", "Kitchen", "Library", "Lounge", "Study"]
    positions = {
        "Ballroom" : (0, 5), 
        "Billiard Room" : (5, 3),
        "Conservatory" : (5, 5),   ##Bind to lounge
        "Dining Room" : (-5, 0),
        "Hall" : (0, -5),
        "Kitchen" : (-5, 5),       ##Bind to study
        "Library" : (5, -2),
        "Lounge" : (-5, -5),       ##Bind to conservatory
        "Study" : (5, -5)          ##Bind to kitchen
        } ##Stores the realtive coordinates for each room with the cellar/root node at (0, 0).
    acc = {
        "suspect": None, 
        "weapon": None, 
        "room": None,
        "type": None ##Type legend:: 0=General Guess; 1=Full accusation; 2=Truth
        }

def SerialiseGame():
    truth = Game_Consts.acc
    truth["suspect"] = random.choice(Game_Consts.suspects)
    truth["weapon"] = random.choice(Game_Consts.weapons)
    truth["room"] = random.choice(Game_Consts.rooms)
    truth["type"] = 2 ##Builds the truth of the murder
    print(truth)

    game = dict(truth)
    game = json.dumps(game) ##Combines all aspects into a single, JSON-Serialised string
    return game

def GameUpdate():
    game = SerialiseGame()
    gitping = github3.login("AXIDE", "MAdddCOdes161204") ##Github initialisation
    repos = gitping.repository(owner="AXIDE", repository="Cluedo")
    repos.file_contents("/gamedata.json").update(f"Updated: {datetime.datetime.now()}", bytes(game.encode("utf-8")))
    return game

def GameQuery():
    game = requests.get("https://raw.github.com/AXIDE/Cluedo/master/gamedata.json").text
    return game

schedule.every().day.at("00:00").do(GameUpdate)
