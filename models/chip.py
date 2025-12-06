from database.db import Database
from mysql.connector import Error


class Chip:
    def __init__(
        self.chip_id=None, chip_player_id=None, chip_tournament_id=None, chip_balance=0
    ) -> None:
        self.chip_id = chip_id
        self.chip_player_id = chip_player_id
        self.chip_tournament_id = chip_tournament_id
        self.chip_balance = chip_balance

    def __repr__(self):
        return f"Chip(player={self.chip_player_id}, balance={self.chip_balance})"

    @staticmethod
    def create(player_id, tournament_id, amount):
        sql = """
        INSERT INTO Chips (chip_player_id, chip_tournament_id, chip_balance)
        VALUES (%s, %s, %s)
        """
        try:
            with Database() as db:
                db.execute(sql, (player_id, tournament_id, amount))
                chip_id = db.cursor.lastrowid
            return Chip(
                chip_id=chip_id,
                chip_player_id=player_id,
                chip_tournament_id=tournament_id,
                chip_balance=amount,
            )
        except Error as e:
            print(f"Database error while creating Chip: {e}")
            return None

    @staticmethod
    def get_by_player_and_tournament(player_id, tournament_id):
        sql = "SELECT * FROM Chips WHERE chip_player_id = %s AND chip_tournament_id = %s"
        try:
            with Database() as db:
                row = db.fetchone(sql, (player_id, tournament_id))
            if row:
                return Chip(**row)
            return None
        except Error as e:
            print(f"Database error while getting Chip: {e}")
            return None

    def update(self):
        sql = """
        UPDATE Chips
        SET chip_balance = %s
        WHERE chip_id = %s
        """
        try:
            with Database() as db:
                db.execute(sql, (self.chip_balance, self.chip_id))
                return True
        except Error as e:
            print(f"Database error while updating Chip: {e}")
            return False
