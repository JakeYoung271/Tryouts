from collections import deque
import tkinter as tk
from tkinter import messagebox

from roster import Roster
from tryoutsManager import TryoutsManager

class TournamentGUI:
    def __init__(self, root, manager):
        self.root = root
        self.root.title("Tournament Manager")
        self.manager = manager
        
        # --- Player Management Frame ---
        player_frame = tk.LabelFrame(root, text="Player Management", padx=10, pady=10)
        player_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Active Player List
        self.active_player_label = tk.Label(player_frame, text="Active players")
        self.active_player_label.grid(row=0, column=0)
        self.active_player_listbox = tk.Listbox(player_frame, height=10)
        self.active_player_listbox.grid(row=1, column=0, columnspan=2)
        
        self.inactive_player_label = tk.Label(player_frame, text="Inactive players")
        self.inactive_player_label.grid(row=0, column=2)
        self.inactive_player_listbox = tk.Listbox(player_frame, height=10)
        self.inactive_player_listbox.grid(row=1, column=2, columnspan=2)
        self.update_player_listbox()

        # Add Player
        tk.Label(player_frame, text="Name:").grid(row=2, column=0)
        self.player_name_entry = tk.Entry(player_frame)
        self.player_name_entry.grid(row=2, column=1)
        tk.Button(player_frame, text="Add Player", command=self.add_player).grid(row=3, column=0, columnspan=2)

        # Rename Player
        tk.Button(player_frame, text="Rename Player", command=self.rename_player).grid(row=4, column=0, columnspan=2)

        # Remove Player
        tk.Button(player_frame, text="Remove Player", command=self.remove_player).grid(row=5, column=0, columnspan=2)

        # Mark Active / Inactive
        tk.Button(player_frame, text="Mark Active", command=self.mark_active).grid(row=6, column=0)
        tk.Button(player_frame, text="Mark Inactive", command=self.mark_inactive).grid(row=6, column=1)

        # --- Pool Management Frame ---
        pool_frame = tk.LabelFrame(root, text="Pool Management", padx=10, pady=10)
        pool_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Create Pool
        tk.Button(pool_frame, text="Create Pool", command=self.create_pool).grid(row=0, column=0, columnspan=2)

        # Manually Create Pool
        tk.Label(pool_frame, text="Player IDs (comma-separated):").grid(row=1, column=0)
        self.pool_players_entry = tk.Entry(pool_frame)
        self.pool_players_entry.grid(row=1, column=1)
        tk.Button(pool_frame, text="Manual Pool", command=self.create_manual_pool).grid(row=2, column=0, columnspan=2)

        # View Pools
        self.pool_listbox = tk.Listbox(pool_frame, height=10)
        self.pool_listbox.grid(row=3, column=0, columnspan=2)
        tk.Button(pool_frame, text="Delete Pool", command=self.delete_pool).grid(row=4, column=0, columnspan=2)

        # --- Score Entry Frame ---
        score_frame = tk.LabelFrame(root, text="Score Entry", padx=10, pady=10)
        score_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Enter Scores
        tk.Label(score_frame, text="Pool ID:").grid(row=0, column=0)
        self.pool_id_entry = tk.Entry(score_frame)
        self.pool_id_entry.grid(row=0, column=1)
        tk.Button(score_frame, text="Choose Pool", command=self.choose_pool).grid(row=1, column=0, columnspan=2)

        self.scores_label_first = tk.Label(score_frame, text="Scores (team1_score, team2_score):")
        self.scores_label_first.grid(row=2, column=0)
        self.scores_entry_first = tk.Entry(score_frame)
        self.scores_entry_first.grid(row=2, column=1)
        self.scores_label_second = tk.Label(score_frame, text="Scores (team1_score, team2_score):")
        self.scores_label_second.grid(row=3, column=0)
        self.scores_entry_second = tk.Entry(score_frame)
        self.scores_entry_second.grid(row=3, column=1)
        self.scores_label_third = tk.Label(score_frame, text="Scores (team1_score, team2_score):")
        self.scores_label_third.grid(row=4, column=0)
        self.scores_entry_third = tk.Entry(score_frame)
        self.scores_entry_third.grid(row=4, column=1)

        self.scores_button_submit = tk.Button(score_frame, text="Submit Scores", command=self.submit_scores)
        self.scores_button_submit.grid(row=5, column=0, columnspan=2)
        
        self.hide_score_entry()

        # --- Ratings Display Frame ---
        ratings_frame = tk.LabelFrame(root, text="Player Ratings", padx=10, pady=10)
        ratings_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.ratings_listbox = tk.Listbox(ratings_frame, height=10)
        self.ratings_listbox.grid(row=0, column=0, columnspan=2)
        self.update_ratings_listbox()
        
    def hide_score_entry(self):
        self.scores_entry_first.grid_forget()
        self.scores_label_first.grid_forget()
        self.scores_entry_second.grid_forget()
        self.scores_label_second.grid_forget()
        self.scores_entry_third.grid_forget()
        self.scores_label_third.grid_forget()
        self.scores_button_submit.grid_forget()
    
    def show_score_entry(self):
        self.scores_entry_first.grid(row=2, column=0)
        self.scores_label_first.grid(row=2, column=1)
        self.scores_entry_second.grid(row=3, column=0)
        self.scores_label_second.grid(row=3, column=1)
        self.scores_entry_third.grid(row=4, column=0)
        self.scores_label_third.grid(row=4, column=1)
        self.scores_button_submit.grid(row=5, column=0)
        

    # --- Player Management Functions ---

    def update_player_listbox(self):
        """Updates the player listbox with active players."""
        self.active_player_listbox.delete(0, tk.END)
        self.inactive_player_listbox.delete(0, tk.END)
        for player_id in self.manager.players:
            player = self.manager.players[player_id]
            status = "Active" if player_id in self.manager.active_players else "Inactive"
            if status == "Active":
                self.active_player_listbox.insert(tk.END, f"{player.name} (ID: {player.id})")
            else:
                self.inactive_player_listbox.insert(tk.END, f"{player.name} (ID: {player.id})")
        self.active_player_label.config(text=f"Active players ({len(self.manager.active_players)})")
        self.inactive_player_label.config(text=f"Inactive players ({len(self.manager.inactive_players)})")

    def add_player(self):
        """Adds a new player."""
        name = self.player_name_entry.get()
        if name:
            self.manager.add_player(name)
            self.update_player_listbox()
            self.update_ratings_listbox()
        else:
            messagebox.showerror("Error", "Player name cannot be empty!")

    def remove_player(self):
        """Removes the selected player."""
        selection = self.inactive_player_listbox.curselection()
        if selection:
            player_info = self.inactive_player_listbox.get(selection[0])
            player_id = int(player_info.split("ID: ")[1].split(")")[0])
            self.manager.remove_player(player_id)
            # self.manager.waiting_players = deque([p for p in self.manager.waiting_players if p != player_id])
            self.update_player_listbox()
            self.update_ratings_listbox()
        else:
            messagebox.showerror("Error", "No inactive player selected!")

    def rename_player(self):
        """Renames the selected player."""
        selection = self.inactive_player_listbox.curselection()
        new_name = self.player_name_entry.get()
        if selection and new_name:
            player_info = self.inactive_player_listbox.get(selection[0])
            player_id = int(player_info.split(" (ID: ")[1].split(")")[0])
            self.manager.rename_player(player_id, new_name)
            self.update_player_listbox()
            self.update_ratings_listbox()
        else:
            messagebox.showerror("Error", "No inactive player selected or name is empty!")

    def mark_active(self):
        """Marks the selected player as active."""
        active_selection = self.active_player_listbox.curselection()
        inactive_selection = self.inactive_player_listbox.curselection()
        if active_selection:
            player_info = self.active_player_listbox.get(active_selection[0])
            player_id = int(player_info.split(" (ID: ")[1].split(')')[0])
            self.manager.mark_active(player_id)
            self.update_player_listbox()
        elif inactive_selection:
            player_info = self.inactive_player_listbox.get(inactive_selection[0])
            player_id = int(player_info.split(" (ID: ")[1].split(')')[0])
            self.manager.mark_active(player_id)
            self.update_player_listbox()
        else:
            messagebox.showerror("Error", "No player selected!")

    def mark_inactive(self):
        """Marks the selected player as inactive."""
        active_selection = self.active_player_listbox.curselection()
        inactive_selection = self.inactive_player_listbox.curselection()
        if active_selection:
            player_info = self.active_player_listbox.get(active_selection[0])
            player_id = int(player_info.split(" (ID: ")[1].split(')')[0])
            self.manager.mark_inactive(player_id)
            self.update_player_listbox()
        elif inactive_selection:
            player_info = self.inactive_player_listbox.get(inactive_selection[0])
            player_id = int(player_info.split(" (ID: ")[1].split(')')[0])
            self.manager.mark_inactive(player_id)
            self.update_player_listbox()
        else:
            messagebox.showerror("Error", "No player selected!")

    # --- Pool Management Functions ---

    def update_pool_listbox(self):
        """Updates the pool listbox with active pools."""
        self.pool_listbox.delete(0, tk.END)
        for index, pool in enumerate(self.manager.current_pools):
            players_in_pool = [self.manager.players[p].name for p in pool]
            self.pool_listbox.insert(tk.END, f"Pool {index} {pool}: {', '.join(players_in_pool)}")

    def create_pool(self):
        """Automatically creates pools from the waiting list."""
        try:
            self.manager.create_pools()
        except ValueError as v:
            messagebox.showerror("Error", v.args[0])
        self.update_pool_listbox()

    def create_manual_pool(self):
        """Manually creates a pool with specific player IDs."""
        player_ids = self.pool_players_entry.get().split(",")
        try:
            player_ids = [int(pid.strip()) for pid in player_ids]
            self.manager.create_manual_pool(player_ids)
            self.update_pool_listbox()
        except ValueError as v:
            messagebox.showerror("Error", v.args[0])

    def delete_pool(self):
        """Deletes the selected pool."""
        selection = self.pool_listbox.curselection()
        if selection:
            pool_info = self.pool_listbox.get(selection[0])
            pool = list(map(int, pool_info.split("Pool ")[1].split(":")[0].strip("[]").split(",")))
            self.manager.delete_pool(pool)
            self.update_pool_listbox()
        else:
            messagebox.showerror("Error", "No pool selected!")

    # --- Score Entry Functions ---
    
    def choose_pool(self):
        self.hide_score_entry()
        pool_id = self.pool_id_entry.get()
        if not pool_id:
            messagebox.showerror("Error", "Pool ID and scores cannot be empty!")
            return
        try:
            pool_id = int(pool_id)
            current_pool = self.manager.current_pools[pool_id]
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid pool ID!")
        self.selected_pool = str(pool_id)
        
        player1, player2, player3, player4 = current_pool
        player1 = self.manager.roster.get_player_by_id(player1)
        player2 = self.manager.roster.get_player_by_id(player2)
        player3 = self.manager.roster.get_player_by_id(player3)
        player4 = self.manager.roster.get_player_by_id(player4)

        
        first_match = f"{player1.name}/{player2.name} vs {player3.name}/{player4.name}"
        
        second_match = f"{player1.name}/{player3.name} vs {player2.name}/{player4.name}"
        
        third_match = f"{player1.name}/{player4.name} vs {player2.name}/{player3.name}"

        self.scores_label_first.config(text=first_match)
        self.scores_label_second.config(text=second_match)
        self.scores_label_third.config(text=third_match)
        
        self.show_score_entry()

    def submit_scores(self):
        """Submits the scores for a pool."""
        pool_id = self.pool_id_entry.get()
        print(pool_id)
        print(self.selected_pool)
        if pool_id != self.selected_pool:
            messagebox.showerror("Error", "Pool ID has changed")
            return
            
        score1 = self.scores_entry_first.get()
        score1 = self.validate_score(score1)
        if not score1:
            messagebox.showerror("Error", "The first score has invalid formatting. Please use the format %d-%d")
            return
            
        
        score2 = self.scores_entry_second.get()
        score2 = self.validate_score(score2)
        if not score2:
            messagebox.showerror("Error", "The second score has invalid formatting. Please use the format %d-%d")
            return
        
        score3 = self.scores_entry_third.get()
        score3 = self.validate_score(score3)
        if not score3:
            messagebox.showerror("Error", "The third score has invalid formatting. Please use the format %d-%d")
            return
        
        self.manager.input_scores(int(pool_id), score1, score2, score3)
        self.update_ratings_listbox()
        self.update_pool_listbox()
        self.hide_score_entry()
            
    def validate_score(self, score: str):
        if score.count("-") != 1:
            return False
        left, right = score.split("-")
        if not left.isdigit() or not right.isdigit():
            return False
        left, right = int(left), int(right)
        if left == right:
            return False
        return (left, right)

    # --- Ratings Display Functions ---

    def update_ratings_listbox(self):
        """Updates the ratings listbox with current player ratings."""
        self.ratings_listbox.delete(0, tk.END)
        for player_id, player in self.manager.players.items():
            self.ratings_listbox.insert(tk.END, f"{player.name} (ID: {player.id}) - Rating: {player.rating}")


if __name__ == "__main__":
    root = tk.Tk()
    roster = Roster.load_roster()  # Load the roster
    manager = TryoutsManager(roster)  # Initialize the tryouts manager
    gui = TournamentGUI(root, manager)
    root.mainloop()
