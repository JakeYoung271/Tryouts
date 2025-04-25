import csv
from player import Player
from roster import Roster

ratings = {"K": 1200, "Q": 1000, "J": 800}
roster = Roster.load_roster()

with open("setup/royals.csv", "r") as file:
    for row in csv.reader(file):
        team, division, first, last, email = row
        if email == "Email":
            continue
        rating = ratings[division[0]]
        p = Player(f"{first} {last}", roster=roster, rating=rating, start_rating=rating)
        p.save()
        
roster.save_roster()