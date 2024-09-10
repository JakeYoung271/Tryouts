class Player:
    def __init__(self, name, id, rating=800):
        self.name = name
        self.rating = rating
        self.id = id
    def setRating(self, newRating):
        self.rating = newRating