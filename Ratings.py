from player import Player
from match import Match
import random
class Ratings:
    def __init__(self, players, matches):
        self.players = players
        self.matches = matches
    def addPlayer(self, player):
        self.players.append(player)
    def addMatch(self, match):
        self.matches.append(match)

    """
    Computes the probability that the matches would occur with the current ratings
    returns the complement of this, which it then attempts to minimize
    """
    def computeLoss(self):
        overallProb = 1
        for match in self.matches:
            prob = match.probabilityOfResult()
            overallProb *= prob
        return 1-overallProb
    def updateRatings(self):
        for player in self.players:
            player.rating = random.randint(800, 1200)
            print(f"{player.name} rating: {player.rating}")