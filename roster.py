import difflib
import os
import pickle
from player import Player
from match import Match

class Roster:
    def __init__(self):
        self.players_by_id = {}
        self.players_by_name = {}
        self.next_id = 1
        self.next_match_id = 1
        
    def print_roster(self):
        print([(k, v) for k, v in self.players_by_id.items()])

    def register_match(self):
        match_id = self.next_match_id
        self.next_match_id += 1
        return match_id

    def register_player(self, player: Player):
        # Assign a new unique ID to the player
        player_id = self.next_id
        self.next_id += 1
        
        # Add player to the two-way mappings
        self.players_by_id[player_id] = player.name
        self.players_by_name[player.name] = player_id
        
        self.save_roster()

        return player_id
    
    def rename_player(self, player: Player, old_name: str, new_name: str) -> bool:
        # Add player to the two-way mappings
        print(self.players_by_id)
        print(self.players_by_name)
        print(old_name)
        player_id = player.id
        if new_name in self.players_by_name:
            return False
        if old_name not in self.players_by_name:
            return False
        del self.players_by_name[old_name]
        self.players_by_id[player_id] = new_name
        self.players_by_name[new_name] = player_id
        
        self.save_roster()

        return True
    
    def delete_player(self, player: Player):
        player_id = player.id
        
        del self.players_by_id[player_id]
        del self.players_by_name[player.name]
        print(self.players_by_id)
        print(self.players_by_name)
        self.save_roster()

    def get_player_by_id(self, player_id):
        if player_id in self.players_by_id:
            return Player.load(player_id)
        else:
            raise ValueError(f"No player found with ID: {player_id}")

    def get_player_by_name(self, name, fuzzy=False) -> Player:
        if name in self.players_by_name:
            player_id = self.players_by_name[name]
            return Player.load(player_id)
        elif fuzzy:
            close_matches = difflib.get_close_matches(name, self.players_by_name.keys(), n=1, cutoff=0.7)
            if close_matches:
                matched_name = close_matches[0]
                player_id = self.players_by_name[matched_name]
                return Player.load(player_id)
            else:
                raise ValueError(f"No close match found for player name: {name}")
        else:
            raise ValueError(f"No player found with name: {name}")

    def save_roster(self):
        # Save the roster mapping for future use
        roster_file_path = os.path.join("data", "roster.pkl")
        with open(roster_file_path, 'wb') as file:
            pickle.dump(self, file)
        print("Roster saved.")

    @staticmethod
    def load_roster():
        roster_file_path = os.path.join("data", "roster.pkl")
        if os.path.exists(roster_file_path):
            with open(roster_file_path, 'rb') as file:
                return pickle.load(file)
        else:
            return Roster()  # Return a new empty Roster if none exists
