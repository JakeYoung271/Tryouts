def getWinProbability(diff):
    return 1 / (1 + 10 ** (-diff / 400))

class Match:
    #result should be 1 if team one wins, 0 if team two wins
    def __init__(self, id, player1, player2, player3, player4, result):
        self.team1 = (player1, player2)
        self.team2 = (player3, player4)
        self.result = result
        self.id = id

    def __str__(self):
        return f"{self.id},{self.team1[0].id},{self.team1[1].id},{self.team2[0].id},{self.team2[1].id},{self.result}"
    
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

    @staticmethod
    def load(match_str, player_dict):
        match_id, player1, player2, player3, player4, result = map(int, match_str.split(","))
        player1 = player_dict[player1]
        player2 = player_dict[player2]
        player3 = player_dict[player3]
        player4 = player_dict[player4]
        return Match(match_id, player1, player2, player3, player4, result)
        