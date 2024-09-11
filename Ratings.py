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
            match.player1.addMatch(match)
            match.player2.addMatch(match)
            match.player3.addMatch(match)
            match.player4.addMatch(match)
        increment = 64
        outerLoops = 0
        innerLoops = 0
        while increment != 0:
            outerLoops += 1
            changeOccurred = False
            dir = 1
            for player in self.players:
                oldProb = player.computeProbabilty()
                player.rating += increment
                newProb = player.computeProbabilty()
                if newProb < oldProb:
                    dir = -1
                    player.rating -= 2 * increment
                    newProb = player.computeProbabilty()
                while newProb > oldProb and player.rating >= 0 and player.rating <= 2500:
                    innerLoops += 1
                    oldProb = newProb
                    player.rating += dir * increment
                    newProb = player.computeProbabilty()
                    changeOccurred = True
                player.rating -= dir * increment
            if player.rating < 0:
                player.rating = 0
            if player.rating > 2500:
                player.rating = 2500
            if not changeOccurred:
                increment /= 2
        self.renormalize()
        print(f"Outer loops: {outerLoops}, Inner loops: {innerLoops}")

    def renormalize(self):
        sum = 0
        for player in self.players:
            sum += player.rating
        sum //= len(self.players)
        diff = 800 - sum
        for player in self.players:
            player.rating += diff
                