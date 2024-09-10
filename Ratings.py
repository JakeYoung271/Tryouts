from player import Player
from match import Match
class Ratings:
    def __init__(self):
        self.players = []
        self.matches = []
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
        pass