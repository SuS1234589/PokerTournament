from database.db import Database
from mysql.connector import Error


class Player:
    def __init__(self, id=None, name=None, email=None, status=None) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.status = status

    @staticmethod
    def create(name, email, status):
        # Check if a player with the same email already exists
        sql = "SELECT * FROM Players WHERE psu_email = %s"
        with Database() as db:
            row = db.fetchone(sql, (email,))
        if row:
            print(f"The player {email} has already been added.")
            return None

        sql = """
        INSERT INTO Players (name, psu_email, status)
        VALUES (%s,%s,%s)
        """
        try:
            with Database() as db:
                db.execute(sql, (name, email, status))
                player_id = db.cursor.lastrowid
            return Player(id=player_id, name=name, email=email, status=status)
        except Error as e:
            print(f"Database error while creating player: {e}")
            return None

    @staticmethod
    def get_by_id(player_id):
        sql = "SELECT * FROM Players WHERE player_id = %s"
        try:
            with Database() as db:
                row = db.fetchone(sql, (player_id,))
            if row:
                return Player(
                    id=row["player_id"],
                    name=row["name"],
                    email=row["psu_email"],
                    status=row["status"],
                )
            return None
        except Error as e:
            print(f"Database error while getting player by ID: {e}")
            return None

    @staticmethod
    def get_all():
        sql = "SELECT * FROM Players"
        try:
            with Database() as db:
                rows = db.fetchall(sql)
            return [
                Player(
                    id=row["player_id"],
                    name=row["name"],
                    email=row["psu_email"],
                    status=row["status"],
                )
                for row in rows
            ]
        except Error as e:
            print(f"Database error while getting all players: {e}")
            return []

    def update(self):
        sql = """
        UPDATE Players
        SET name = %s, psu_email = %s, status = %s
        WHERE player_id = %s
        """
        try:
            with Database() as db:
                db.execute(sql, (self.name, self.email, self.status, self.id))
                return True
        except Error as e:
            print(f"Database error while updating player: {e}")
            return False

    def delete(self):
        cleanup_queries = [
            "DELETE FROM Chips WHERE chip_player_id = %s",
            "DELETE FROM SeatingAssignments WHERE seating_player_id = %s",
            "DELETE FROM GameActions WHERE game_player_id = %s",
            "DELETE FROM Registration WHERE registered_player_id = %s",
            "DELETE FROM Players WHERE player_id = %s",
        ]

        try:
            with Database() as db:
                for sql in cleanup_queries:
                    db.execute(sql, (self.id,))
                return True
        except Error as e:
            print(f"Error: Could not delete player with ID {self.id}.")
            print(
                "This is likely because the player is still referenced in other tables."
            )
            print(f"Original database error: {e}")
            return False
