from models.tournament import Tournament
from models.registration import Registration
from models.player import Player
from database.db import Database


def _get_validated_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")


def create_tournament():
    name = input("Tournament Name: ")
    descr = input("Description: ")
    organizer_id = _get_validated_int_input("Organizer Player ID: ")
    
    organizer = Player.get_by_id(organizer_id)
    if not organizer:
        print(f"Error: Organizer ID {organizer_id} does not exist.")
        return

    tournament = Tournament.create(name, descr, organizer_id)
    if tournament:
        print(f"Successfully created tournament: {tournament.name} (ID: {tournament.tournament_id})")
    else:
        print("Failed to create tournament.")

def view_tournaments():
    tournaments = Tournament.get_all()
    if not tournaments:
        print("No tournaments found.")
        return

    print(f"\n{'ID':<5} {'Name':<30} {'Organizer ID'}")
    print("-" * 50)
    for t in tournaments:
        print(f"{t.tournament_id:<5} {t.name:<30} {t.organizer_id}")
    print()

def remove_tournament():
    t_id = _get_validated_int_input("Enter Tournament ID to delete: ")
    tournament = Tournament.get_by_id(t_id)
    
    if tournament:
        if tournament.delete():
            print(f"Tournament {t_id} deleted.")
        else:
            print("Error: Could not delete tournament (It might have active games/registrations).")
    else:
        print("Tournament not found.")

def register_player():
    player_id = _get_validated_int_input("Player ID: ")
    tournament_id = _get_validated_int_input("Tournament ID: ")
    buyin = _get_validated_int_input("Buyin Amount: ")

    if not Player.get_by_id(player_id):
        print("Error: Player not found.")
        return
    if not Tournament.get_by_id(tournament_id):
        print("Error: Tournament not found.")
        return

    regis = Registration.create(player_id, tournament_id, buyin, "Registered")
    if regis:
        print(f"Player {player_id} registered for tournament {tournament_id}.")
    else:
        print("Failed to register player.")


def remove_player_from_tournament():
    player_id = _get_validated_int_input("Player ID to remove: ")
    tournament_id = _get_validated_int_input("Tournament ID: ")
    
    regis = Registration.get_by_player_and_tournament(player_id, tournament_id)

    if regis:
        if regis.delete():
            print("Player removed from tournament.")
        else:
            print("Error: Failed to delete registration.")
    else:
        print("Registration not found.")

def list_registered_players():
    print("\n--- Registered Players ---")
    registrations = Registration.get_all()
    if not registrations:
        print("No players registered.")
        return

    for reg in registrations:
        try:
            player = reg.get_player() 
            tournament = reg.get_tournament()
            p_name = player.name if player else "Unknown"
            t_name = tournament.name if tournament else "Unknown"
            
            print(f"Player: {p_name} (ID: {reg.registered_player_id}) -> {t_name} (ID: {reg.registered_tournament_id})")
        except AttributeError:
            print(f"Reg ID: {reg.registration_id} | Player ID: {reg.registered_player_id}")
    print("--------------------------\n")

def assign_seat(tournament_id, table_id, player_id, seat_num):
    # validate that table exists
    sql_check = "SELECT 1 FROM Tables WHERE table_id = %s"
    
    try:
        with Database() as db:
            row = db.fetchone(sql_check, (table_id,))
            if not row:
                print(f"Error: Table {table_id} does not exist. Create it first!")
                return False

            sql_insert = """
            INSERT INTO SeatingAssignments (seating_tournament_id, seating_table_id, seating_player_id, seat_number)
            VALUES (%s, %s, %s, %s)
            """
            db.execute(sql_insert, (tournament_id, table_id, player_id, seat_num))
            print(f"Player {player_id} seated at Table {table_id}, Seat {seat_num}.")
            return True
    except Exception as e:
        print(f"Error seating player: {e}")
        return False