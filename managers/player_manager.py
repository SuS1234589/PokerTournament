from models.player import Player 

def add_player(id, name, email, status):
    Player.create(id, name, email, status)

def view_players():
    return Player.get_all() 

def view_player(id):
    return Player.get_by_id(id)

def remove_player(id):
    player = Player.get_by_id(id)
    if player:
        player.delete()
