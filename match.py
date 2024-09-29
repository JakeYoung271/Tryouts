from player import Player

def getWinProbability(diff):
    return 1 / (1 + 10 ** (-diff / 400))

class Match:
    #result should be 1 if team one wins, 0 if team two wins
    def __init__(self, player1, player2, player3, player4, team1_score, team2_score):
        self.team1 = [player1, player2]
        self.team2 = [player3, player4]
        self.result = int(team1_score > team2_score)
        self.id = id
        self.matches = []

    def __str__(self):
        return f"Match {self.id}: {self.team1[0].name}, {self.team1[1].name}, {self.team2[0].name}, {self.team2[1].name}, {self.result}"
    def getRatingDiff(self):
        return (self.team1[0].rating + self.team1[1].rating - self.team2[0].rating - self.team2[1].rating)/2
    def probabilityOfResult(self):
        diff = self.getRatingDiff()
        if self.result == 1:
            return getWinProbability(diff)
        elif self.result == 0:
            return 1 - getWinProbability(diff)
        else:
            return 0
    def addMatch(self, match):
        self.matches.append(match)