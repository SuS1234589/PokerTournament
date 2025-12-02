import sys
# Import your specific manager functions
from managers.player_manager import add_player, view_players, remove_player
from managers.tournament_manager import (
    create_tournament, 
    register_player, 
    list_registered_players,
    remove_player_from_tournament
)

def print_menu():
    print("\n--- POKER TOURNAMENT SYSTEM ---")
    print("1. Create New Player")
    print("2. View All Players")
    print("3. Delete Player")
    print("4. Create Tournament")
    print("5. Register Player for Tournament")
    print("6. View Registrations")
    print("7. Remove Player from Tournament")
    print("8. Exit")
    print("-------------------------------")

def main():
    while True:
        print_menu()
        choice = input("Enter choice (1-8): ")

        if choice == '1':
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            add_player(name, email, "Active")
            print("Player added successfully.")
        
        elif choice == '2':
            players = view_players()
            print("\n[Player List]")
            for p in players:
                print(f"ID: {p.id} | Name: {p.name} | Status: {p.status}")

        elif choice == '3':
            p_id = int(input("Enter Player ID to delete: "))
            remove_player(p_id)
            print("Player deleted (if they existed).")

        elif choice == '4':
            create_tournament()

        elif choice == '5':
            register_player()

        elif choice == '6':
            list_registered_players()

        elif choice == '7':
            remove_player_from_tournament()

        elif choice == '8':
            print("Goodbye!")
            sys.exit()
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
