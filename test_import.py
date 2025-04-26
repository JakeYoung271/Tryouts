import csv
from player import Player
from roster import Roster

roster = Roster.load_roster()

players = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
]

for i in range(3):
    for j in range(4):
        p = Player(players[4*i+j], roster=roster, rating=800+i*200, start_rating=800+i*200)
        p.save()
        
roster.save_roster()