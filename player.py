MIN_RATING = 0
MAX_RATING = 2500
class Player:
    def __init__(self, name, id, rating=800, present = False):
        self.name = name
        self.rating = rating
        self.gamesPlayed = 0
        self.present = present
        self.id = id
        self.matches = []
    
    def __str__(self):
        return f"{self.name}: {self.rating}, has played {len(self.matches)} games"
    def setRating(self, newRating):
        self.rating = newRating
    def addMatch(self, match):
        self.matches.append(match)
    def computeProbabilty(self, increment=0):
        self.rating += increment
        overallProb = 1
        for match in self.matches:
            prob = match.probabilityOfResult()
            overallProb *= prob
        self.rating -= increment
        return overallProb
    def optimizeRating(self, increment):
        lastProb = self.computeProbabilty()
        newProb = self.computeProbabilty(increment)
        increased = False
        while newProb > lastProb:
            increased = True
            self.rating += increment
            if self.rating >= MAX_RATING:
                self.rating = MAX_RATING
                return
            lastProb = newProb
            newProb = self.computeProbabilty(increment)
        if not increased:
            newProb = self.computeProbabilty(-increment)
            while newProb > lastProb:
                self.rating -= increment
                if self.rating <= MIN_RATING:
                    self.rating = MIN_RATING
                    return
                lastProb = newProb
                newProb = self.computeProbabilty(-increment)