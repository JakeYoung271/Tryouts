import os

def create_data_directory_structure():
    # Get the path of the directory where the script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the top-level directory (assuming `setup` directory is one level deeper)
    top_level_directory = os.path.join(script_directory, "..")
    
    # Define the path for the 'data' directory and its subdirectories
    data_directory = os.path.join(top_level_directory, "data")
    players_directory = os.path.join(data_directory, "players")
    matches_directory = os.path.join(data_directory, "matches")
    rounds_directory = os.path.join(data_directory, "rounds")

    # Create the directories if they do not exist
    os.makedirs(players_directory, exist_ok=True)
    os.makedirs(matches_directory, exist_ok=True)
    os.makedirs(rounds_directory, exist_ok=True)

    print(f"Data directory structure created at: {data_directory}")

if __name__ == "__main__":
    create_data_directory_structure()
