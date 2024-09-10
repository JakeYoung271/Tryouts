from match import Match
from player import Player
from ratings import Ratings

class Pool:
    def __init__(self, player1, player2, player3, player4, id):
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.player4 = player4
        self.id = id
        self.matches = []
    
    def createMatches(self, results = [1,1,1]):
        self.matches.append(Match(self.player1, self.player2, self.player3, self.player4, results[0]))
        self.matches.append(Match(self.player1, self.player3, self.player2, self.player4, results[1]))
        self.matches.append(Match(self.player1, self.player4, self.player2, self.player3, results[2]))
    
    def makeGrid(self):
        col1 = [f"Pool {self.id}", self.player1.id, self.player2.id, self.player3.id, self.player4.id]
        col2 = ["names", self.player1.name, self.player2.name, self.player3.name, self.player4.name]
        grid = [col1, col2]
        for index, match in enumerate(self.matches):
            col = [f"Match {index+1}"]
            names = ", ".join([player.name for player in match.team1])
            col.append(names)
            col.append("vs")
            names = ", ".join([player.name for player in match.team2])
            col.append(names)
            grid.append(col)
            grid.append([f"result{index+1}"])
        return grid
    def insert_2x2_list(self, ws):
        start_col = "A"
        cols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        data = self.makeGrid()
        start_row = self.id * 6 + 1
        for i in range(len(data)):
            for j in range(len(data[i])):
                col_letter = cols[i]
                ws[f"{col_letter}{start_row + j}"] = data[i][j]
    
    def __str__(self):
        return f"Pool {self.id}: {self.player1.name}, {self.player2.name}, {self.player3.name}, {self.player4.name}, {[match.result for match in self.matches]}"
