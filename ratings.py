from player import Player
from match import Match
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
    """
    def computeLoss(self):
        overallProb = 1
        for match in self.matches:
            prob = match.probabilityOfResult()
            overallProb *= prob
        return overallProb
    def updateRatings(self):
        print(len(self.players))
        print(len(self.matches))
        for match in self.matches:
            match.team1[0].addMatch(match)
            match.team1[1].addMatch(match)
            match.team2[0].addMatch(match)
            match.team2[1].addMatch(match)
        increment = 64
        while increment != 0:
            changeOccurred = False
            dir = 1
            for player in self.players:
                player.optimizeRating(increment)
            if not changeOccurred:
                increment //= 2

    def renormalize(self):
        sum = 0
        for player in self.players:
            sum += player.rating
        sum //= len(self.players)
        diff = 800 - sum
        for player in self.players:
            player.rating += diff
                