from models.table import Table
from models.tournament import Tournament
from database.db import Database

def _get_input(prompt):
    return input(prompt)

def create_table():
    print("\n--- Create New Table ---")
    t_id = _get_input("Tournament ID: ")
    
    if not Tournament.get_by_id(t_id):
        print("Error: Tournament not found.")
        return

    seats = _get_input("Max Seats: ")
    
    table = Table.create(t_id, seats, "Open")
    if table:
        print(f"Success: Table (ID: {table.table_id}) created.")
    else:
        print("Failed to create table.")

def list_tables_by_tournament():
    print("\n--- View Tables ---")
    t_id = _get_input("Enter Tournament ID to view tables: ")
    
    tables = Table.get_by_tournament_id(t_id)
    
    if not tables:
        print(f"No tables found for Tournament {t_id}.")
        return

    print(f"\n{'ID':<5} {'Number':<10} {'Status':<15} {'Seats'}")
    print("-" * 40)
    for t in tables:
        print(f"{t.table_id:<5} {t.table_number:<10} {t.registration_status:<15} {t.max_seats}")
    print()

def delete_table():
    print("\n--- Delete Table ---")
    tab_id = _get_input("Enter Table ID to delete: ")
    
    table = Table.get_by_id(tab_id)
    if not table:
        print("Error: Table not found.")
        return
        
    confirm = _get_input(f"Are you sure you want to delete Table {table.table_number}? (Y/N): ")
    if confirm.upper() == 'Y':
        if table.delete():
            print("Table deleted successfully.")
        else:
            print("Error: Could not delete table.")
    else:
        print("Action cancelled.")

def view_seats_at_table():
    print("\n--- View Seated Players ---")
    tab_id = _get_input("Enter Table ID: ")
    
    if not Table.get_by_id(tab_id):
        print("Error: Table not found.")
        return

    seats = Table.get_seated_players(tab_id)
    
    if not seats:
        print(f"Table {tab_id} is currently empty.")
        return

    print(f"\n{'Seat':<5} {'ID':<5} {'Name':<20} {'Email'}")
    print("-" * 50)
    for s in seats:
        print(f"{s['seat_number']:<5} {s['player_id']:<5} {s['name']:<20} {s['psu_email']}")
    print()