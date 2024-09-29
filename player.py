import os
import pickle
import statistics

MIN_RATING = 0
MAX_RATING = 2500

class Player:
    def __init__(self, name, roster, rating=800):
        self.name = name
        self.rating = rating
        self.gamesPlayed = 0
        self.id = roster.register_player(self)  # Register with the Roster and get a unique ID
        self.matches = []
        self.is_active = True

    def setRating(self, newRating):
        self.rating = newRating

    def addMatch(self, match):
        self.matches.append(match)

    def computeProbabilty(self, increment=0):
        self.rating += increment

        # update this to take into account likelihood of an extreme rating.

        overallProb = statistics.NormalDist(800, 400).cdf(self.rating)
        if overallProb > 0.5:
            overallProb -= 0.5
        for match in self.matches:
            prob = match.probabilityOfResult()
            overallProb *= prob
        self.rating -= increment
        return overallProb
    def optimizeRating(self, increment):
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
        players_directory = os.path.join("data", "players")
        if not os.path.exists(players_directory):
            os.makedirs(players_directory)
        
        player_file_path = os.path.join(players_directory, f"{self.id}.pkl")

        with open(player_file_path, 'wb') as file:
            pickle.dump(self, file)
        print(f"Player data saved to {player_file_path}")

    @staticmethod
    def load(player_id):
        player_file_path = os.path.join("data", "players", f"{player_id}.pkl")

        if not os.path.exists(player_file_path):
            raise FileNotFoundError(f"No player data found for ID: {player_id}")

        with open(player_file_path, 'rb') as file:
            return pickle.load(file)

        print(f"Player data loaded from {player_file_path}")
