import re
from models.player import Player 

def is_valid_psu_email(email):
    return re.match(r"[^@]+@psu\.edu$", email)

def add_player(name, email, status):
    if not is_valid_psu_email(email):
        print(f"Error: '{email}' is not a valid PSU email. Player not created.")
        return False
        
    if Player.create(name, email, status):
        print(f"Success: Player '{name}' created.")
        return True
    return False

def view_players():
    return Player.get_all() 

def view_player(id):
    return Player.get_by_id(id)

def remove_player(id):
    player = Player.get_by_id(id)
    if player:
        if player.delete():
            print(f"Success: Player {id} deleted.")
        else:
            print("Error: Could not delete player (Check foreign keys).")
    else:
        print("Error: Player not found.")