import sys
import time
import os

# Import Admin Logic
from managers.player_manager import add_player, view_players, remove_player
from managers.tournament_manager import create_tournament, register_player, list_registered_players, remove_player_from_tournament

# Import Player Logic
from models.hands import run_poker_simulation

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ==========================================
# ADMIN INTERFACE
# ==========================================
def admin_portal():
    while True:
        clear_screen()
        print("=== ADMIN PANEL ===")
        print("1. Add Player")
        print("2. View Players")
        print("3. Delete Player")
        print("4. Create Tournament")
        print("5. Register Player")
        print("6. View Registrations")
        print("7. Remove Registration")
        print("8. Logout")
        
        choice = input("\nAdmin Command: ")

        if choice == '1':
            name = input("Name: ")
            email = input("Email: ")
            add_player(name, email, "Active")
            input("Saved. Press Enter...")
        
        elif choice == '2':
            players = view_players()
            print(f"\n{'ID':<5} {'Name':<20} {'Email'}")
            print("-" * 40)
            for p in players:
                print(f"{p.id:<5} {p.name:<20} {p.email}")
            input("\nPress Enter...")

        elif choice == '3':
            pid = input("Player ID to delete: ")
            if pid.isdigit(): remove_player(int(pid))
        
        elif choice == '4':
            create_tournament()
            input("Press Enter...")
        
        elif choice == '5':
            register_player()
            input("Press Enter...")

        elif choice == '6':
            list_registered_players()
            input("Press Enter...")

        elif choice == '7':
            remove_player_from_tournament()
            input("Press Enter...")

        elif choice == '8':
            break

# ==========================================
# PLAYER INTERFACE
# ==========================================
def player_portal():
    while True:
        clear_screen()
        print("=== PLAYER PORTAL ===")
        print("1. View My Stats")
        print("2. Sit at Table (Simulate Hand)")
        print("3. Logout")

        choice = input("\nAction: ")

        if choice == '1':
            # You could connect this to `view_player(id)` later
            print("\nStats: 0 Wins, 500 Chips")
            input("Press Enter...")
        
        elif choice == '2':
            # This calls the logic from 'hands.py'
            run_poker_simulation()
        
        elif choice == '3':
            break

# ==========================================
# MAIN ROUTER
# ==========================================
if __name__ == "__main__":
    while True:
        clear_screen()
        print("Welcome to the Poker Tournament System")
        print("1. Admin Login")
        print("2. Player Login")
        print("3. Quit")
        
        role = input("\nSelect Role: ")

        if role == '1':
            admin_portal()
        elif role == '2':
            player_portal()
        elif role == '3':
            print("Goodbye.")
            sys.exit()