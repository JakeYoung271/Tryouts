import random
import itertools
from collections import deque
from player import Player
from roster import Roster

class TryoutsManager:
    def __init__(self, roster: Roster):
        self.roster = roster  # Reference to the Roster instance
        self.players = {}  # Stores all players (ID -> Player instance)
        self.active_players = set()  # Stores the IDs of active players
        self.inactive_players = set()  # Stores the IDs of inactive players
        self.waiting_players = deque()  # Queue of players waiting to be added to a pool
        self.current_pools = []  # List of current active pools (list of player IDs)
        self.sit_out_players = []  # Players who have sat out the last pool
        self.load_players()
        self.update_activity()
        
    def update_activity(self):
        for k, v in self.players.items():
            if v.is_active:
                self.active_players.add(k)
                self.waiting_players.append(k)
            else:
                self.inactive_players.add(k)
        
    def load_players(self):
        self.players = {}
        for k in self.roster.players_by_id.keys():
            self.players[k] = Player.load(k)
    
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
        try:
            player = self.roster.get_player_by_name(name)
            print(f"Player {player.name} with ID {player.id} already exists")
        except ValueError:
            new_player = Player(name=name, roster=self.roster)
            self.players[new_player.id] = new_player
            self.active_players.add(new_player.id)
            self.waiting_players.append(new_player.id)
            new_player.save()
            print(f"Added player {name} with ID {new_player.id}")
    
    
    def rename_player(self, player_id, new_name):
        """Renames a player by name"""
        player = self.roster.get_player_by_id(player_id)
        old_name = player.name
        player.rename(new_name)
        player.save()
        success = self.roster.rename_player(player, old_name, new_name)
        if success and player.id in self.players:
            self.players[player.id].name = new_name
            print(f"Player {player.id} {old_name} renamed to {new_name}")
        else:
            print(f"Player with ID {player.id} not found.")
    
    def mark_active(self, player_id):
        """Marks a player as active and adds them to the waiting list."""
        player = self.roster.get_player_by_id(player_id)
        player_name = player.name
        player.is_active = True
        player.save()
        if player_id in self.players:
            self.active_players.add(player_id)
            self.inactive_players.discard(player_id)
            if player_id not in self.waiting_players:
                self.waiting_players.append(player_id)
            print(f"Player {player_id} with name {player_name} marked as active.")
        else:
            print(f"Player with ID {player_id} and Name {player_name} not found.")
    
    def mark_inactive(self, player_id):
        """Marks a player as inactive."""
        player = self.roster.get_player_by_id(player_id)
        player_name = player.name
        player.is_active = False
        player.save()
        if player_id in self.players:
            self.active_players.discard(player_id)
            self.inactive_players.add(player_id)
            self.waiting_players = deque([p for p in self.waiting_players if p != player_id])
            print(f"Player {player_id} with name {player_name} marked as inactive.")
        else:
            print(f"Player with ID {player_id} and Name {player_name} not active.")
            
    def list_active_players(self) -> None:
        """Lists all currently active players"""
        [print(self.roster.get_player_by_id(i).name, i) for i in self.active_players]
        
    def check_is_active(self, player_name) -> bool:
        return self.roster.get_player_by_name(player_name).id in self.active_players
        
    
    def create_pools(self) -> None:
        """Creates pools of 4 players from the waiting list."""
        if self.current_pools:
            raise ValueError(f"Remove existing pools before automatically creating new ones")
        if len(self.waiting_players) < 4:
            raise ValueError(f"{len(self.waiting_players)} players are not enough to create a pool automatically")
        while len(self.waiting_players) >= 4:
            pool = [self.waiting_players.popleft() for _ in range(4)]
            self.current_pools.append(pool)
            print(f"Created pool with players: {[self.players[p].name for p in pool]}")

        # Handle sit-out scenario if fewer than 4 players remain
        if 0 < len(self.waiting_players) < 4:
            self.sit_out_players = list(self.waiting_players)
            print(f"Players sitting out this round: {[self.players[p].name for p in self.sit_out_players]}")
    
    def create_manual_pool(self, player_ids: list[str] | list[int]) -> None:
        """
        Manually creates a pool with specified players. Will do so even if pools already exist and haven't been resolved.
        :param player_ids: List of player IDs or names.
        """
        # Validate pool size
        if len(player_ids) != 4:
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
        return (self.roster.get_player_by_id(id).name, self.roster.get_player_by_id(id).id)
    
    def print_pools(self):
        for ind, pool in enumerate(self.current_pools):
            print(ind, [(self.roster.get_player_by_id(i).name,i) for i in pool])

    def input_scores(self, pool_index, p1p2vp3p4, p1p3vp2p4, p1p4vp2p3) -> None:
        """
        Inputs the scores for a specific pool and calculates the new ratings.
        Scores are expected in the form:
        """
        player1, player2, player3, player4 = self.current_pools[pool_index]
        player1 = self.roster.get_player_by_id(player1)
        player2 = self.roster.get_player_by_id(player2)
        player3 = self.roster.get_player_by_id(player3)
        player4 = self.roster.get_player_by_id(player4)
            
        self.update_ratings((player1, player2), (player3, player4), p1p2vp3p4)
        self.update_ratings((player1, player3), (player2, player4), p1p3vp2p4)
        self.update_ratings((player1, player4), (player2, player3), p1p4vp2p3)
        
        # Remove the pool after processing
        self.delete_pool(self.current_pools[pool_index])
        print(f"Pool {pool_index} processed and removed.")
    
    def update_ratings(self, team1, team2, score) -> None:
        """
        Placeholder for actual rating logic.
        """
        team1_score, team2_score = score
        # Adjust ratings based on scores (this is a simplified placeholder)
        for player in team1:
            player.rating += (team1_score - team2_score)  # Adjust by the score difference
            player.save()
        for player in team2:
            player.rating -= (team1_score - team2_score)
            player.save()
        self.load_players()
        print(f"Ratings updated for players in teams: {team1[0].name}/{team1[1].name}, {team2[0].name}/{team2[1].name}")

    def fairness_system(self) -> None:
        """
        Ensure that players who sat out get priority in the next round.
        Players who sat out previously will be added back to the waiting list first.
        """
        for player_id in self.sit_out_players:
            if player_id not in self.waiting_players:
                self.waiting_players.appendleft(player_id)
        self.sit_out_players = []  # Reset the sit-out list for the next round

    def delete_pool(self, pool) -> None:
        """Deletes a pool and adds the players back to the waiting list."""
        if pool in self.current_pools:
            for player_id in pool:
                if player_id not in self.waiting_players:
                    self.waiting_players.append(player_id)
            self.current_pools.remove(pool)
            print(f"Pool {pool} deleted, and players re-added to the waiting list.")
        else:
            print("Pool not found.")
    
    def print_player_status(self) -> None:
        """Prints the status of all players (active, waiting, and in pools)."""
        print(f"Active players: {[self.players[p].name for p in self.active_players]}")
        print(f"Waiting players: {[self.players[p].name for p in self.waiting_players]}")
        print(f"Current pools: {self.current_pools}")