import gzip
import os
import pickle
import statistics
import math

from match import Match

MIN_RATING = 0
MAX_RATING = 2500

class Player:
    def __init__(self, name, roster, rating=800):
        self.name = name
        self.rating = rating
        self.id = roster.register_player(self)  # Register with the Roster and get a unique ID
        self.matches = []
        self.is_active = True
        self.games_played = 0
        self.wins = 0
        self.losses = 0

    def update_members(self):
        self.games_played = len(self.matches)
        self.wins = 0
        self.losses = 0

        for match in self.matches:
            if type(match) == str:
                player1, player2, player3, player4, result = [int(i) for i in match.split(",")[1:]]
                if player1 == self.id or player2 == self.id:
                    if result == 1:
                        self.wins += 1
                    else:
                        self.losses += 1
                else:
                    if result == 0:
                        self.wins += 1
                    else:
                        self.losses += 1
            if type(match)==Match:
                if match.team1[0].id == self.id or match.team1[1].id == self.id:
                    if match.result == 1:
                        self.wins += 1
                    else:
                        self.losses += 1
                else:
                    if match.result == 0:
                        self.wins += 1
                    else:
                        self.losses += 1
    def setRating(self, newRating):
        self.rating = newRating

    def addMatch(self, match):
        self.matches.append(match)
        self.games_played = len(self.matches)

        # not sure if match is a string or a Match object
        # can take out update members to just increment wins or losses
        # but left it in because it checks if the object is a string or not first and looks cleaner
        # even though it resets the wins and losses every time

        
    def updateMatch(self, match_id, match):
        for i in range(len(self.matches)):
            if self.matches[i].id == match_id:
                self.matches[i] = match
                return
        

    def computeProbabilty(self, increment=0):
        self.rating += increment

        # update this to take into account likelihood of an extreme rating.

        overallProb = statistics.NormalDist(800, 400).cdf(self.rating)
        if overallProb > 0.5:
            overallProb = 1 - overallProb
        overallProb **= 1/4
        for match in self.matches:
            prob = match.probabilityOfResult()
            overallProb *= prob
        self.rating -= increment
        # print(overallProb)
        return overallProb
    
    def optimizeRating(self, increment):
        print(f"Optimizing rating for {self.name}")
        initialRating = self.rating
        lastProb = self.computeProbabilty()
        newProb = self.computeProbabilty(increment)
        increased = False
        while newProb > lastProb:
            increased = True
            self.rating += increment
            if self.rating >= MAX_RATING:
                self.rating = MAX_RATING
                return initialRating != self.rating
            lastProb = newProb
            newProb = self.computeProbabilty(increment)
        if not increased:
            newProb = self.computeProbabilty(-increment)
            while newProb > lastProb:
                self.rating -= increment
                if self.rating <= MIN_RATING:
                    self.rating = MIN_RATING
                    return initialRating != self.rating
                lastProb = newProb
                newProb = self.computeProbabilty(-increment)
        return initialRating != self.rating
    
    def rename(self, new_name):
        self.name = new_name
        
    def delete(self):
        players_directory = os.path.join("data", "players")
        if not os.path.exists(players_directory):
            os.makedirs(players_directory)
        
        player_file_path = os.path.join(players_directory, f"{self.id}.pkl")

        os.remove(player_file_path)
        print(f"Player data in {player_file_path} deleted")        
    
    def save(self):
        temp = self.matches
        self.matches = [str(match) for match in self.matches]
        players_directory = os.path.join("data", "players")
        if not os.path.exists(players_directory):
            os.makedirs(players_directory)

        player_file_path = os.path.join(players_directory, f"{self.id}.pkl.gz")
        with gzip.open(player_file_path, 'wb') as file:
            pickle.dump(self, file, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"Player data saved to {player_file_path} with compression")
        self.matches = temp

    @staticmethod
    def load(player_id):
        player_file_path = os.path.join("data", "players", f"{player_id}.pkl.gz")
        if not os.path.exists(player_file_path):
            raise FileNotFoundError(f"No player data found for ID: {player_id}")

        with gzip.open(player_file_path, 'rb') as file:
            p = pickle.load(file)
            p.update_members()
            return p
        print(f"Player data loaded from {player_file_path} with compression")


if __name__ == "__main__":
    with gzip.open("data/1.pkl.gz", 'rb') as file:
        p = pickle.load(file)
        import sys
        n = sys.getrefcount(p)
        t = p.matches
        a = 0