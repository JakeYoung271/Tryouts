from collections import deque
import tkinter as tk
from tkinter import messagebox
import threading
from tkinter import ttk
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

        self.pool_swap_label = tk.Label(pool_frame, text="Swap probability")
        self.pool_swap_label.grid(row=5, column=0)        
        self.pool_swap_prob = tk.Entry(pool_frame)
        self.pool_swap_prob.insert(0, "0.33")
        self.pool_swap_prob.grid(row=5, column=1)
        
        self.pool_swap_loops_label = tk.Label(pool_frame, text="Swap loops")
        self.pool_swap_loops_label.grid(row=6, column=0)
        self.pool_swap_loops = tk.Entry(pool_frame)
        self.pool_swap_loops.insert(0, "5")
        self.pool_swap_loops.grid(row=6, column=1)

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
        
        self.ratings_button = tk.Button(ratings_frame, text="Update ratings", command=self.update_ratings)
        self.ratings_button.grid(row=0, column=2)
        self.update_ratings_listbox()
        
        # --- Matches Display Frame ---
        matches_frame = tk.LabelFrame(root, text="Matches", padx=10, pady=10)
        matches_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        self.matches_listbox = tk.Listbox(matches_frame, height=10)
        self.matches_listbox.grid(row=0, column=0, columnspan=1)
        self.update_matches_listbox()
        
        # --- Matches Edit Frame
        matches_edit_frame = tk.LabelFrame(root, text="Edit Matches", pady=10, padx=10)
        matches_edit_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
         
        # Enter Scores
        tk.Label(matches_edit_frame, text="Match ID:").grid(row=0, column=0)
        self.match_id_entry = tk.Entry(matches_edit_frame)
        self.match_id_entry.grid(row=0, column=1)
        tk.Button(matches_edit_frame, text="Choose Match", command=self.choose_match).grid(row=1, column=0, columnspan=2)

        self.match_label = tk.Label(matches_edit_frame, text="Scores (team1_score, team2_score):")
        self.match_label.grid(row=2, column=0)
        self.match_entry = tk.Entry(matches_edit_frame)
        self.match_entry.grid(row=2, column=1)

        self.match_button_submit = tk.Button(matches_edit_frame, text="Submit Scores", command=self.submit_match)
        self.match_button_submit.grid(row=5, column=0, columnspan=2)
        
        self.hide_match_entry()
        
    def hide_match_entry(self):
        self.match_entry.grid_forget()
        self.match_button_submit.grid_forget()
        self.match_label.grid_forget()
    
    def show_match_entry(self):
        self.match_entry.grid(row=2, column=1)
        self.match_button_submit.grid(row=5, column=0, columnspan=2)
        self.match_label.grid(row=2, column=0)
        
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
                self.active_player_listbox.insert(tk.END, f"{player.name} (ID: {player.id}) G:{player.games_played}")
            else:
                self.inactive_player_listbox.insert(tk.END, f"{player.name} (ID: {player.id}) G:{player.games_played}")
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
            self.pool_listbox.insert(tk.END, f"Pool {index}: {','.join(players_in_pool)}: {pool}")

    def create_pool(self):
        """Automatically creates pools from a multiple of 4"""
        
        try:
            sp = float(self.pool_swap_prob.get())
            l = int(self.pool_swap_loops.get())
            if sp < 0 or sp > 1:
                raise ValueError
            if l < 0:
                raise ValueError     
        except ValueError as v:
            messagebox.showerror("Error", "Please use a value between 0 and 1 for swap probability and a positive integer for loops")
            return
        try:
            self.manager.create_pools(sp, l)
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
            # print(pool_info)
            # print(pool_info.split(" ")[2].split(":")[0].strip("[]").split(","))
            pool = list(map(int, pool_info.split(": ")[2].strip("[]").split(",")))
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
        except (ValueError, IndexError, KeyError):
            messagebox.showerror("Error", "Invalid pool ID!")
        self.selected_pool = str(pool_id)
        
        player1, player2, player3, player4 = current_pool
        player1 = self.manager.players[player1]
        player2 = self.manager.players[player2]
        player3 = self.manager.players[player3]
        player4 = self.manager.players[player4]

        
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
            self.pool_id_entry.delete(0, len(str(pool_id)))
            self.hide_score_entry()
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
        self.update_player_listbox()
        self.update_matches_listbox()
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

    def update_ratings(self):
        self.manager.update_ratings()
        self.update_ratings_listbox()

    def update_ratings_listbox(self):
        """Updates the ratings listbox with current player ratings."""
        self.ratings_listbox.delete(0, tk.END)
        for player_id, player in self.manager.players.items():
            self.ratings_listbox.insert(tk.END, f"{player.name[:min(len(player.name), 10)]}: {player.rating}")
            
            
    # --- Match management functions ---
    def update_matches_listbox(self):
        """Updates the matches listbox with latest matches"""
        self.matches_listbox.delete(0, tk.END)
        for match_id, match in self.manager.matches.items():
            self.matches_listbox.insert(tk.END, f"{match_id}: {match.team1[0].name}/{match.team1[1].name} {'beat' if match.result == 1 else 'lost to'} {match.team2[0].name}/{match.team2[1].name}")
            
            
    def choose_match(self):
        match_id = self.match_id_entry.get()
        if not match_id or match_id:
            messagebox.showerror("Error", "Match cannot be empty!")
            return
        try:
            match_id = int(match_id)
            current_match = self.manager.matches[match_id]
        except (ValueError, IndexError, KeyError):
            messagebox.showerror("Error", "Invalid match ID!")
        self.selected_match = str(match_id)
        
        player1, player2 = current_match.team1
        player3, player4 = current_match.team2

        
        match_text = f"{player1.name}/{player2.name} vs {player3.name}/{player4.name}"

        self.match_label.config(text=match_text)
        
        self.show_match_entry()
        
    def submit_match(self):
        """Submits the score for a match."""
        match_id = self.match_id_entry.get()
        if match_id != self.selected_match:
            messagebox.showerror("Error", "Match ID has changed")
            self.match_id_entry.delete(0, len(str(match_id)))
            self.hide_match_entry()
            return
        
        score = self.match_entry.get()
        score = self.validate_score(score)
        if not score:
            messagebox.showerror("Error", "The 'Edit Match' score has invalid formatting. Please use the format %d-%d")
            return
        
        self.manager.update_score(int(match_id), score)
        self.update_matches_listbox()
        self.hide_match_entry() 


if __name__ == "__main__":
    root = tk.Tk()
    roster = Roster.load_roster()  # Load the roster
    manager = TryoutsManager(roster)  # Initialize the tryouts manager
    gui = TournamentGUI(root, manager)
    def save_player_data(manager, save_window, progress_bar):
        # Save player data (this should be a non-blocking operation)
        manager.save()  # Replace with your actual save logic
        
        # Close the progress bar and root window safely in the main thread
        def on_save_complete():
            progress_bar.stop()
            save_window.destroy()
            root.quit()  # Use root.quit() instead of root.destroy() to safely exit the main loop
        
        # Schedule the UI update using `after` to run on the main thread
        root.after(0, on_save_complete)

    def on_closing():
        # Create a pop-up window for the saving message
        save_window = tk.Toplevel(root)
        save_window.title("Saving Data")
        save_window.geometry("300x100")
        
        # Display a message
        label = tk.Label(save_window, text="Saving player data, please wait...")
        label.pack(pady=10)
        
        # Create and pack a progress bar
        progress_bar = ttk.Progressbar(save_window, orient="horizontal", mode="indeterminate", length=250)
        progress_bar.pack(pady=5)
        progress_bar.start()  # Start the progress bar animation

        # Run the save operation in a separate thread
        threading.Thread(target=save_player_data, args=(manager, save_window, progress_bar)).start()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
