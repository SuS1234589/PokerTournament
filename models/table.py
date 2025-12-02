from database.db import Database
from mysql.connector import Error

class Table:
    def __init__(
        self,
        table_id=None,
        tournament_id=None,
        table_number=None,
        max_seats=None,
        registration_status=None,
    ) -> None:
        self.table_id = table_id
        self.tournament_id = tournament_id
        self.table_number = table_number
        self.max_seats = max_seats
        self.registration_status = registration_status

    def __repr__(self):
        return f"Table(id={self.table_id}, number={self.table_number})"

    @staticmethod
    def create(tournament_id, table_number, max_seats, registration_status):
        sql = """
        INSERT INTO Tables (table_tournament_id, table_number, max_seats, player_registration_status)
        VALUES (%s, %s, %s, %s)
        """
        try:
            with Database() as db:
                db.execute(
                    sql, (tournament_id, table_number, max_seats, registration_status)
                )
                # Capture the auto-increment ID
                t_id = db.cursor.lastrowid
            
            return Table(
                table_id=t_id,
                tournament_id=tournament_id,
                table_number=table_number,
                max_seats=max_seats,
                registration_status=registration_status,
            )
        except Error as e:
            print(f"Database error while creating Table: {e}")
            return False

    @staticmethod
    def get_by_id(table_id):
        sql = "SELECT * FROM Tables WHERE table_id = %s"
        try:
            with Database() as db:
                row = db.fetchone(sql, (table_id,))
            if row:
                return Table(
                    table_id=row['table_id'],
                    tournament_id=row['table_tournament_id'],
                    table_number=row['table_number'],
                    max_seats=row['max_seats'],
                    registration_status=row['player_registration_status']
                )
            return None
        except Error as e:
            print(f"Database error while getting table by ID: {e}")
            return None

    @staticmethod
    def get_all():
        sql = "SELECT * FROM Tables"
        try:
            with Database() as db:
                rows = db.fetchall(sql)
            
            return [
                Table(
                    table_id=row['table_id'],
                    tournament_id=row['table_tournament_id'],
                    table_number=row['table_number'],
                    max_seats=row['max_seats'],
                    registration_status=row['player_registration_status']
                ) for row in rows
            ]
        except Error as e:
            print(f"Database error while getting all Tables: {e}")
            return []

    def update(self):
        sql = """
        UPDATE Tables
        SET table_tournament_id = %s, table_number = %s, max_seats = %s, player_registration_status = %s
        WHERE table_id = %s
        """
        try:
            with Database() as db:
                db.execute(
                    sql,
                    (
                        self.tournament_id,
                        self.table_number,
                        self.max_seats,
                        self.registration_status,
                        self.table_id,
                    ),
                )
                return True
        except Error as e:
            print(f"Database error while updating Table: {e}")
            return False

    def delete(self):
        sql = "DELETE FROM Tables WHERE table_id = %s"
        try:
            with Database() as db:
                db.execute(sql, (self.table_id,))
                return True
        except Error as e:
            print(f"Database error while deleting Table: {e}")
            return False