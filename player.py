import gzip
import os
import pickle
import statistics

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

    def setRating(self, newRating):
        self.rating = newRating

    def addMatch(self, match):
        self.matches.append(match)
        self.games_played = len(self.matches)
        

    def computeProbabilty(self, increment=0):
        self.rating += increment

        # update this to take into account likelihood of an extreme rating.

        overallProb = statistics.NormalDist(800, 400).cdf(self.rating)
        if overallProb > 0.5:
            overallProb = 1 - overallProb
        overallProb = 1
        for match in self.matches:
            prob = match.probabilityOfResult()
            overallProb *= prob
        self.rating -= increment
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
        self.matches = [str(match) for match in self.matches]
        players_directory = os.path.join("data", "players")
        if not os.path.exists(players_directory):
            os.makedirs(players_directory)

        player_file_path = os.path.join(players_directory, f"{self.id}.pkl.gz")
        with gzip.open(player_file_path, 'wb') as file:
            pickle.dump(self, file, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"Player data saved to {player_file_path} with compression")

    @staticmethod
    def load(player_id):
        player_file_path = os.path.join("data", "players", f"{player_id}.pkl.gz")
        if not os.path.exists(player_file_path):
            raise FileNotFoundError(f"No player data found for ID: {player_id}")

        with gzip.open(player_file_path, 'rb') as file:
            p = pickle.load(file)
            p.games_played = len(p.matches)
            return p
        print(f"Player data loaded from {player_file_path} with compression")


if __name__ == "__main__":
    with gzip.open("data/1.pkl.gz", 'rb') as file:
        p = pickle.load(file)
        import sys
        n = sys.getrefcount(p)
        t = p.matches
        a = 0