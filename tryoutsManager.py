from collections import Counter
import csv
import random
from match import Match
from player import Player
from roster import Roster

class TryoutsManager:
    def __init__(self, roster: Roster):
        self.roster = roster  # Reference to the Roster instance
        self.players = {}  # Stores all players (ID -> Player instance)
        self.active_players = set()  # Stores the IDs of active players
        self.inactive_players = set()  # Stores the IDs of inactive players
        self.current_pools = []  # List of current active pools (list of player IDs)
        self.sit_out_players = []  # Players who have sat out the last pool
        self.matches = {}
        self.load_players()
        self.update_activity()      
                    
    def save(self):
        for player in self.players.values():
            player.save()
        
    def update_activity(self):
        for k, v in self.players.items():
            if v.is_active:
                self.active_players.add(k)
            else:
                self.inactive_players.add(k)
        
    def load_players(self):
        self.players = {}
        for k in self.roster.players_by_id.keys():
            self.players[k] = Player.load(k)
        for k, v in self.players.items():
            v.matches = [Match.load(match, self.players) for match in v.matches]
            for m in v.matches:
                self.matches[m.id] = m
    
    def print_ratings(self):
        for k, v in self.players.items():
            print(k, v.name, v.rating)
        
    def remove_player(self, player_id):
        player = self.players.pop(player_id)
        self.inactive_players.discard(player_id)
        self.roster.delete_player(player)
        player.delete()
        
    def add_player(self, name):
        """Adds a new player and marks them as active."""
        # try:
        #     player = self.roster.get_player_by_name(name)
        #     print(f"Player {player.name} with ID {player.id} already exists")
        # except ValueError:
        new_player = Player(name=name, roster=self.roster)
        self.players[new_player.id] = new_player
        self.active_players.add(new_player.id)
        print(f"Added player {name} with ID {new_player.id}")
    
    
    def rename_player(self, player_id, new_name):
        """Renames a player by name"""
        player = self.players[player_id]
        old_name = player.name
        player.rename(new_name)
        success = self.roster.rename_player(player, old_name, new_name)
        if success and player.id in self.players:
            self.players[player.id].name = new_name
            print(f"Player {player.id} {old_name} renamed to {new_name}")
        else:
            print(f"Player with ID {player.id} not found.")
        player.save()
    
    def mark_active(self, player_id):
        """Marks a player as active"""
        player = self.players[player_id]
        player_name = player.name
        player.is_active = True
        if player_id in self.players:
            self.active_players.add(player_id)
            self.inactive_players.discard(player_id)
            print(f"Player {player_id} with name {player_name} marked as active.")
        else:
            print(f"Player with ID {player_id} and Name {player_name} not found.")
    
    def mark_inactive(self, player_id):
        """Marks a player as inactive."""
        player = self.players[player_id]
        player_name = player.name
        player.is_active = False
        if player_id in self.players:
            self.active_players.discard(player_id)
            self.inactive_players.add(player_id)
            print(f"Player {player_id} with name {player_name} marked as inactive.")
        else:
            print(f"Player with ID {player_id} and Name {player_name} not active.")
            
    def list_active_players(self) -> None:
        """Lists all currently active players"""
        [print(self.players[i].name, i) for i in self.active_players]
    
    def create_pools(self, swap_prob=0, num_loops=0) -> None:
        """Creates pools of 4 players from the active list."""
        if self.current_pools:
            raise ValueError(f"Remove existing pools before automatically creating new ones")
        if len(self.active_players) % 4 != 0 or len(self.active_players) < 4:
            raise ValueError(f"Need active players to be a multiple of 4 to create pools")
        
        player_ratings = []
        
        for k in self.active_players:
            player_ratings.append((self.players[k].rating, k))
            
        player_ratings.sort()
        
        if swap_prob and num_loops:
            for i in range(num_loops):
                for j in range(len(player_ratings)-1):
                    if random.random() < swap_prob:
                        player_ratings[j], player_ratings[j+1] = player_ratings[j+1], player_ratings[j]
        
        while player_ratings:
            pool = []
            for i in range(4):
                pool.append(player_ratings.pop()[1])
            self.current_pools.append(pool)
            
    def create_manual_pool(self, player_ids: list[str] | list[int]) -> None:
        """
        Manually creates a pool with specified players. Will do so even if pools already exist and haven't been resolved.
        :param player_ids: List of player IDs or names.
        """
        # Validate pool size
        if len(player_ids) != 4 or len(Counter(player_ids).keys()) != 4:
            raise ValueError("Pools must contain exactly 4 players.")
        
        # Convert names to IDs if necessary
        pool = []
        for player in player_ids:
            if isinstance(player, int) and player in self.players:
                pool.append(player)
            elif isinstance(player, str):
                player_id = self.roster.players_by_name.get(player)
                if player_id:
                    pool.append(player_id)
                else:
                    raise ValueError(f"Player {player} not found.")
            else:
                raise ValueError(f"Player ID {player} not found.")
        
        # Check if players are active and not already in a pool
        for player_id in pool:
            if player_id not in self.active_players:
                raise ValueError(f"Player {self.players[player_id].name} is inactive.")
            for existing_pool in self.current_pools:
                if player_id in existing_pool:
                    raise ValueError(f"Player {self.players[player_id].name} is already in an active pool.")

        # Add the manually created pool
        self.current_pools.append(pool)
        print(f"Manually created pool with players: {[self.players[p].name for p in pool]}")
        
    def get_name_and_id(self, id): 
        return (self.players[id].name, id)
    
    def print_pools(self):
        for ind, pool in enumerate(self.current_pools):
            print(ind, [(self.players[i].name,i) for i in pool])
            
    def update_score(self, match_index, score):
        team1_score, team2_score = score
        result = int(team1_score > team2_score)
        
        if self.matches[match_index].result == result:
            return
        self.matches[match_index].result = result
        
        match = self.matches[match_index]
        match.team1[0].updateMatch(match_index, match)
        match.team1[1].updateMatch(match_index, match)
        match.team2[0].updateMatch(match_index, match)
        match.team2[1].updateMatch(match_index, match)

    def input_scores(self, pool_index, p1p2vp3p4, p1p3vp2p4, p1p4vp2p3) -> None:
        """
        Inputs the scores for a specific pool and calculates the new ratings.
        Scores are expected in the form:
        """
        player1, player2, player3, player4 = self.current_pools[pool_index]
        player1 = self.players[player1]
        player2 = self.players[player2]
        player3 = self.players[player3]
        player4 = self.players[player4]
        
        self.add_matches((player1, player2), (player3, player4), p1p2vp3p4)
        self.add_matches((player1, player3), (player2, player4), p1p3vp2p4)
        self.add_matches((player1, player4), (player2, player3), p1p4vp2p3)
        
        # Remove the pool after processing
        self.delete_pool(self.current_pools[pool_index])

        print(f"Pool {pool_index} processed and removed.")
    
    def update_ratings(self) -> None:
        players = self.players.values()
        increment = 64
        while increment != 0:
            changed = False
            for player in players:
                changed = player.optimizeRating(increment) or changed
            if not changed:
                increment //= 2
        for player in players:
            player.update_members()

    def add_matches(self, team1, team2, score) -> None:
        """
        Placeholder for actual rating logic.
        """
        team1_score, team2_score = score
        match = Match(self.roster.register_match(), team1[0], team1[1], team2[0], team2[1], int(team1_score > team2_score))
        # Adjust ratings based on scores (this is a simplified placeholder)
        for player in team1:
            player.addMatch(match)
            player.save()
        for player in team2:
            player.addMatch(match)
            player.save()
        print(f"Ratings updated for players in teams: {team1[0].name}/{team1[1].name}, {team2[0].name}/{team2[1].name}")

    def delete_pool(self, pool) -> None:
        """Deletes a pool."""
        if pool in self.current_pools:
            self.current_pools.remove(pool)
            print(f"Pool {pool} deleted")
        else:
            print("Pool not found.")
    
    def print_player_status(self) -> None:
        """Prints the status of all players (active, inactive and in pools)."""
        print(f"Active players: {[self.players[p].name for p in self.active_players]}")
        print(f"Active players: {[self.players[p].name for p in self.inactive_players]}")
        print(f"Current pools: {self.current_pools}")
        
        
if __name__ == "__main__":
    pass