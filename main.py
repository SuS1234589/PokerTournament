import sys
import time
import os

from managers.player_manager import add_player, view_players, view_player, remove_player
from managers.tournament_manager import (
    create_tournament, 
    view_tournaments, 
    remove_tournament,
    register_player, 
    list_registered_players, 
    remove_player_from_tournament,
    assign_seat 
)
from models.table import Table 
from models.hands import run_poker_simulation
from managers.table_manager import create_table, list_tables_by_tournament, delete_table, view_seats_at_table

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    clear_screen()
    print("=" * 40)
    print(f"{title:^40}")
    print("=" * 40)
    print()

def pause():
    input("\nPress Enter to continue...")

def get_menu_choice(options, exit_option=True):
    for key, value in options.items():
        print(f"{key}. {value}")
    
    if exit_option:
        print("B. Back")
        print("X. Exit System")
    
    print("-" * 40)
    return input("Select Option: ").upper()

# ==========================================
# SUB-MENUS (ADMIN)
# ==========================================

def menu_admin_players():
    while True:
        print_header("ADMIN > PLAYERS")
        options = {
            '1': 'Create New Player (PSU Email Only)',
            '2': 'View All Players',
            '3': 'Delete Player'
        }
        choice = get_menu_choice(options)

        if choice == '1':
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            add_player(name, email, "Active")
            pause()
        
        elif choice == '2':
            players = view_players()
            print(f"\n{'ID':<5} {'Name':<20} {'Email'}")
            print("-" * 40)
            for p in players:
                print(f"{p.id:<5} {p.name:<20} {p.email}")
            pause()

        elif choice == '3':
            pid = input("Enter Player ID to delete: ")
            if pid.isdigit():
                remove_player(int(pid))
            else:
                print("Invalid ID.")
            pause()

        elif choice == 'B': return
        elif choice == 'X': sys.exit()

def menu_admin_tournaments():
    while True:
        print_header("ADMIN > TOURNAMENTS")
        options = {
            '1': 'Create Tournament',
            '2': 'View Tournaments',
            '3': 'Delete Tournament',
            '4': 'Register Player',
            '5': 'List Registrations',
            '6': 'Remove Player from Tournament'
        }
        choice = get_menu_choice(options)

        if choice == '1':
            create_tournament()
            pause()
        elif choice == '2':
            view_tournaments()
            pause()
        elif choice == '3':
            remove_tournament()
            pause()
        elif choice == '4':
            register_player()
            pause()
        elif choice == '5':
            list_registered_players()
            pause()
        elif choice == '6':
            remove_player_from_tournament()
            pause()
        elif choice == 'B': return
        elif choice == 'X': sys.exit()

def menu_admin_tables():
    while True:
        print_header("ADMIN > TABLES")
        options = {
            '1': 'Create New Table',
            '2': 'View Tables (by Tournament)',
            '3': 'Delete Table',
            '4': 'Assign Seat (Force Sit)',
            '5': 'View Seated Players at Table'
        }
        choice = get_menu_choice(options)

        if choice == '1':
            create_table()
            pause()
        
        elif choice == '2':
            list_tables_by_tournament()
            pause()

        elif choice == '3':
            delete_table()
            pause()
        
        elif choice == '4':
            print("--- Assign Seat ---")
            tour_id = input("Tournament ID: ")
            tab_id = input("Table ID: ")
            p_id = input("Player ID: ")
            seat = input("Seat Number: ")
            assign_seat(tour_id, tab_id, p_id, seat)
            pause()

        elif choice == '5':
            view_seats_at_table()
            pause()

        elif choice == 'B': return
        elif choice == 'X': sys.exit()

# ==========================================
# MAIN PORTALS
# ==========================================

def admin_portal():
    while True:
        print_header("ADMIN DASHBOARD")
        options = {
            '1': 'Manage Players',
            '2': 'Manage Tournaments',
            '3': 'Manage Tables',
        }
        choice = get_menu_choice(options)

        if choice == '1': menu_admin_players()
        elif choice == '2': menu_admin_tournaments()
        elif choice == '3': menu_admin_tables()
        elif choice == 'B': return
        elif choice == 'X': sys.exit()

def player_portal():
    while True:
        print_header("PLAYER PORTAL")
        options = {
            '1': 'My Profile',
            '2': 'Sit at Table (Play Hand)',
        }
        choice = get_menu_choice(options)

        if choice == '1':
            try:
                p_id = int(input("Enter your Player ID: "))
                player = view_player(p_id)
                if player:
                    print(f"\n--- PROFILE: {player.name} ---")
                    print(f"ID: {player.id}")
                    print(f"Email: {player.email}")
                    print(f"Status: {player.status}")
                else:
                    print("Player not found.")
            except ValueError:
                print("Invalid ID.")
            pause()
            
        elif choice == '2':
            try:
                p_id = int(input("Enter your Player ID: "))
                # CONSTANT 1 FOR DEMO PURPOSES
                # in real app it should automatically find your seat
                run_poker_simulation(player_id=p_id, table_id=1) 
            except ValueError:
                print("Invalid ID.")
                time.sleep(1)
        
        elif choice == 'B': return
        elif choice == 'X': sys.exit()

# ==========================================
# MAIN ROUTER
# ==========================================
if __name__ == "__main__":
    while True:
        print_header("POKER TOURNAMENT SYSTEM")
        print("1. Admin Login")
        print("2. Player Login")
        print("X. Exit")
        print("-" * 40)
        
        role = input("Select Role: ").upper()

        if role == '1':
            admin_portal()
        elif role == '2':
            player_portal()
        elif role == 'X':
            print("Shutting down!")
            sys.exit()
