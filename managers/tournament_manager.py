from models.tournament import Tournament
from models.registration import Registration

BUYING_AMOUNT = 500
STATUS = "Registered"


def _get_validated_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")


def create_tournament():
    name = input("What is the name of the Tournament: ")
    descr = input("What is the description of the Tournament: ")
    organizer_id = _get_validated_int_input("What is the organizer's player ID: ")
    tournament = Tournament.create(name, descr, organizer_id)
    if tournament:
        print(f"Successfully created tournament: {tournament.name}")
    else:
        print("Failed to create tournament.")


def register_player():
    player_id = _get_validated_int_input("What is the player ID: ")
    tournament_id = _get_validated_int_input("What is the tournament ID: ")
    regis = Registration.create(player_id, tournament_id, BUYING_AMOUNT, STATUS)
    if regis:
        print(f"Player {player_id} has been registered for tournament {tournament_id}.")
    else:
        print("Failed to register player.")


def remove_player_from_tournament():
    player_id = _get_validated_int_input("What is the player ID to remove: ")
    tournament_id = _get_validated_int_input(
        "What is the tournament ID to remove them from: "
    )
    regis = Registration.get_by_player_and_tournament(player_id, tournament_id)

    if regis:
        if regis.delete():
            print("The player was successfully removed from the tournament.")
        else:
            print("Error: Failed to delete the registration.")
    else:
        print("Could not find a registration for that player and tournament.")


def list_registered_players():
    print("\n--- Registered Players ---")
    registrations = Registration.get_all()
    if not registrations:
        print("No players are currently registered for any tournament.")
        return

    for reg in registrations:
        player = reg.get_player()
        tournament = reg.get_tournament()
        player_name = player.name if player else "Unknown Player"
        tournament_name = tournament.name if tournament else "Unknown Tournament"
        print(
            f"- Player: {player_name} (ID: {reg.registered_player_id}) | "
            f"Tournament: {tournament_name} (ID: {reg.registered_tournament_id}) | "
            f"Status: {reg.registered_status}"
        )
    print("--------------------------\n")
