class Player:
    def __init__(self, name, id, rating=800, present = False):
        self.name = name
        self.rating = rating
        self.gamesPlayed = 0
        self.present = present
        self.id = id
        self.matches = []
    def setRating(self, newRating):
        self.rating = newRating
    def addMatch(self, match):
        self.matches.append(match)
    def computeProbabilty(self):
        overallProb = 1
        for match in self.matches:
            prob = match.probabilityOfResult()
            overallProb *= prob
        return overallProb