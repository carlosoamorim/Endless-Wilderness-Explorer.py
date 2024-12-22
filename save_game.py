import pickle
import os
import json
SAVE_FILE = "savegame.pkl"




def save_game(player, current_round, enemies_per_round):
    """
    Save the game state to a file.
    """
    game_state = {
        "player_health": player.current_health,
        "player_max_health": player.max_health,
        "player_speed": player.speed,
        "player_wallet": player.wallet,
        "current_round": current_round,
        "enemies_per_round": enemies_per_round
    }

    # Save to a file
    with open("save_game.json", "w") as save_file:
        json.dump(game_state, save_file)

    # Debug print to confirm save
    print("Game Saved!")
    print(f"Player Health: {player.current_health}/{player.max_health}")
    print(f"Player Speed: {player.speed}")
    print(f"Player Wallet: {player.wallet}")
    print(f"Current Round: {current_round}")
    print(f"Enemies Per Round: {enemies_per_round}")


def load_game(player):
    """
    Load the game state from a file.
    """
    try:
        with open("save_game.json", "r") as save_file:
            game_state = json.load(save_file)

            # Load player stats
            player.current_health = game_state["player_health"]
            player.max_health = game_state["player_max_health"]
            player.speed = game_state["player_speed"]
            player.wallet = game_state["player_wallet"]

            # Debug print to confirm load
            print("Game Loaded!")
            print(f"Player Health: {player.current_health}/{player.max_health}")
            print(f"Player Speed: {player.speed}")
            print(f"Player Wallet: {player.wallet}")
            print(f"Current Round: {game_state['current_round']}")
            print(f"Enemies Per Round: {game_state['enemies_per_round']}")

            return game_state["current_round"], game_state["enemies_per_round"]
    except FileNotFoundError:
        print("No save file found. Starting a new game.")
        return 1, 5  # Default round and enemies per round

def reset_save():
    """
    Reset the save file to start a new game.
    """
    try:
        os.remove("save_game.json")
        print("Save file reset successfully!")
    except FileNotFoundError:
        print("No save file found to reset.")

