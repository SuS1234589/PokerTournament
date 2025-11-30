from database.db import Database
from mysql.connector import Error
from models.player import Player
from models.tournament import Tournament


class Registration:
    def __init__(
        self,
        registration_id=None,
        registered_player_id=None,
        registered_tournament_id=None,
        buyin_amount=None,
        registered_status=None,
    ) -> None:
        self.registration_id = registration_id
        self.registered_player_id = registered_player_id
        self.registered_tournament_id = registered_tournament_id
        self.buyin_amount = buyin_amount
        self.registered_status = registered_status

    def get_player(self):
        return Player.get_by_id(self.registered_player_id)

    def get_tournament(self):
        return Tournament.get_by_id(self.registered_tournament_id)

    @staticmethod
    # This function is to register players. should change the name and variable names to make it easier
    def create(
        registered_player_id, registered_tournament_id, buyin_amount, registered_status
    ):
        sql = """
        INSERT INTO Registration(registered_player_id, registered_tournament_id, buyin_amount, registered_status)
        VALUES (%s,%s,%s,%s)
        """
        try:
            with Database() as db:
                db.execute(
                    sql,
                    (
                        registered_player_id,
                        registered_tournament_id,
                        buyin_amount,
                        registered_status,
                    ),
                )
                r_id = db.cursor.lastrowid
            return Registration(
                registration_id=r_id,
                registered_player_id=registered_player_id,
                registered_tournament_id=registered_tournament_id,
                buyin_amount=buyin_amount,
                registered_status=registered_status,
            )
        except Error as e:
            print(f"Database Error while creating Registration entry: {e}")
            return False

    @staticmethod
    def get_by_id(r_id):
        """Gets a single registration entry by its ID."""
        sql = """
        SELECT * FROM Registration WHERE registration_id=%s 
        """
        try:
            with Database() as db:
                row = db.fetchone(sql, (r_id,))
            if row:
                return Registration(**row)
            return None
        except Error as e:
            print(f"Database error while getting registration by ID: {e}")
            return None

    @staticmethod
    def get_all():
        sql = "SELECT * FROM Registration"
        try:
            with Database() as db:
                rows = db.fetchall(sql)
            return [Registration(**row) for row in rows]
        except Error as e:
            print(f"Database error while getting all Registration: {e}")
            return []

    @staticmethod
    def get_by_player_and_tournament(r_id, t_id):
        sql = """
        SELECT * FROM Registration
        WHERE registered_player_id = %s AND registered_tournament_id = %s
        """
        try:
            with Database() as db:
                row = db.fetchone(sql, (r_id, t_id))
            if row:
                return Registration(**row)
        except Error as e:
            print(
                f"Database error while getting registration from player and tournament: {e}"
            )
            return False

    def update(self):
        sql = """
        UPDATE Registration 
        SET registered_player_id = %s, registered_tournament_id = %s, buyin_amount = %s, registered_status = %s 
        WHERE registration_id = %s
        """
        try:
            with Database() as db:
                db.execute(
                    sql,
                    (
                        self.registered_player_id,
                        self.registered_tournament_id,
                        self.buyin_amount,
                        self.registered_status,
                        self.registration_id,
                    ),
                )
                return True
        except Error as e:
            print(f"Database error while updating registration: {e}")
            return False

    def delete(self):
        sql = "DELETE FROM Registration WHERE registration_id = %s"
        try:
            with Database() as db:
                db.execute(sql, (self.registration_id,))
                return True
        except Error as e:
            print(f"Database error while deleting registration: {e}")
            return False

    def delete_player(self):
        sql = """
        DELETE FROM Registration
        WHERE registered_player_id = %s 
        AND registered_tournament_id = %s
        """
        try:
            with Database() as db:
                db.execute(
                    sql, (self.registered_player_id, self.registered_tournament_id)
                )
                return True
        except Error as e:
            print(f"Database error while deleting registered player: {e}")
            return False
