from database.db import Database
from mysql.connector import Error


class Player:
    def __init__(
        self, player_id=None, player_name=None, player_email=None, player_status=None
    ) -> None:
        self.id = player_id
        self.name = player_name
        self.email = player_email  # only psu email
        self.status = player_status

    @staticmethod
    def create(name, email, status):
        sql = """
        INSERT INTO Players (name, psu_email, status)
        VALUES (%s,%s,%s)
        """
        try:
            with Database() as db:
                db.execute(sql, (name, email, status))
                player_id = db.cursor.lastrowid
            return Player(
                player_id=player_id, player_name=name, player_email=email, player_status=status
            )
            return True
        except Error as e:
            print(f"Database error while creating player: {e}")
            return False

    @staticmethod
    def get_by_id(player_id):
        sql = "SELECT * FROM Players WHERE player_id = %s"
        try:
            with Database() as db:
                row = db.fetchone(sql, (player_id,))
            if row:
                return Player(**row)
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
            return [Player(**row) for row in rows]
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
        sql = "DELETE FROM Players WHERE player_id = %s"
        try:
            with Database() as db:
                db.execute(sql, (self.id,))
            return True
        except Error as e:
            print(f"Database error while deleting player: {e}")
            return False
