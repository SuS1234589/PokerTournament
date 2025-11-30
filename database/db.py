# database/db.py
# CHANGE PASSWORD
import mysql.connector
import os


class Database:
    def __init__(
        self,
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD", "admin"),
        database="PokerTournament",
    ):
        self.conn = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        # rows as dicts: {"player_id": 1, "name": "...", ...}
        self.cursor = self.conn.cursor(dictionary=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def execute(self, sql, params=None):
        """Run INSERT/UPDATE/DELETE."""
        self.cursor.execute(sql, params or [])
        self.conn.commit()

    def fetchone(self, sql, params=None):
        """Run a SELECT that returns a single row."""
        self.cursor.execute(sql, params or [])
        return self.cursor.fetchone()

    def fetchall(self, sql, params=None):
        """Run a SELECT that returns multiple rows."""
        self.cursor.execute(sql, params or [])
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
