class Player:
    def __init__(self, name, id, rating=800, present = False):
        self.name = name
        self.rating = rating
        self.gamesPlayed = 0
        self.present = present
        self.id = id
    def setRating(self, newRating):
        self.rating = newRating