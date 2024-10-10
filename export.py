import csv
from roster import Roster
from tryoutsManager import TryoutsManager

roster = Roster().load_roster()
manager = TryoutsManager(roster)

manager.load_players()

with open("data/players.csv", "w", newline="") as file:
    writer = csv.writer(file, delimiter=',')
    rows = []
    players = sorted(manager.players.values(), key=lambda x: x.rating, reverse=True)
    for player in players:
        rows.append([player.name, str(player.rating), player.games_played])
    rows.insert(0, ["Name", "Rating", "Games"])
    writer.writerows(rows)