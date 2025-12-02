import random
from models.registration import Registration
from models.table import Table
from models.seating_assignment import SeatingAssignment
from models.player import Player
from models.tournament import Tournament
from models.chip import Chip


def assign_seats_randomly(tournament_id):
    """
    Assigns all registered players in a tournament to tables randomly
    and gives them their starting chip stack.
    """
    print("Assigning seats and distributing chips...")

    tourn = Tournament.get_by_id(tournament_id)
    if not tourn or not tourn.starting_chips:
        print("Tournament not found or has no starting_chips defined.")
        return

    registrations = Registration.get_by_tournament(tournament_id)
    if not registrations:
        print("No registered players to assign.")
        return

    player_ids = [reg.registered_player_id for reg in registrations]
    random.shuffle(player_ids)
    player_iterator = iter(player_ids)

    tables = Table.get_by_tournament(tournament_id)
    if not tables:
        print("No tables available for this tournament.")
        return

    all_players_seated = False
    for table in tables:
        if all_players_seated:
            break
        print(f"Assigning players to Table {table.table_number}...")
        for _ in range(table.max_seats):
            player_id = next(player_iterator, None)
            if player_id:
                # 1. Assign seat
                SeatingAssignment.create(tournament_id, table.table_id, player_id)
                # 2. Create chip stack
                Chip.create(player_id, tournament_id, tourn.starting_chips)
            else:
                all_players_seated = True
                break
    print("Seat and chip assignment complete.")


def print_table_layout(tournament_id):
    """
    Prints the seating layout for all tables in a tournament.
    """
    print(f"\n--- Seating Layout for Tournament {tournament_id} ---")
    tables = Table.get_by_tournament(tournament_id)
    if not tables:
        print("No tables found for this tournament.")
        return

    for table in tables:
        print(f"\nTable {table.table_number}:")
        assignments = SeatingAssignment.get_by_table(table.table_id)

        seated_players = {}
        if assignments:
            for assign in assignments:
                player = Player.get_by_id(assign.player_id)
                if player:
                    seated_players[assign.seat_number] = player.name

        for i in range(1, table.max_seats + 1):
            player_name = seated_players.get(i, "EMPTY")
            print(f"   Seat {i}: {player_name}")
    print("\n--- End of Layout ---")



