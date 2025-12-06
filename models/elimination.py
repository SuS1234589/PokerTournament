from database.db import Database
from mysql.connector import Error


class Elimination:
    def __init__(
        self,
        elimination_id=None,
        eliminated_player_id=None,
        eliminated_tournament_id=None,
        elimination_round=None,
        position=None,
    ) -> None:
        self.elimination_id = elimination_id
        self.eliminated_player_id = eliminated_player_id
        self.eliminated_tournament_id = eliminated_tournament_id
        self.elimination_round = elimination_round
        self.position = position

    def __repr__(self):
        return (
            f"Elimination(player={self.eliminated_player_id}, "
            f"tournament={self.eliminated_tournament_id}, "
            f"position={self.position})"
        )

    @staticmethod
    def create(player_id, tournament_id, elimination_round, position):
        sql = """
        INSERT INTO Eliminations (eliminated_player_id, eliminated_tournament_id, elimination_round, position)
        VALUES (%s, %s, %s, %s)
        """
        try:
            with Database() as db:
                db.execute(sql, (player_id, tournament_id, elimination_round, position))
                elimination_id = db.cursor.lastrowid
            return Elimination(
                elimination_id=elimination_id,
                eliminated_player_id=player_id,
                eliminated_tournament_id=tournament_id,
                elimination_round=elimination_round,
                position=position,
            )
        except Error as e:
            print(f"Database error while creating Elimination: {e}")
            return None

    @staticmethod
    def get_by_tournament(tournament_id):
        sql = "SELECT * FROM Eliminations WHERE eliminated_tournament_id = %s ORDER BY position ASC"
        try:
            with Database() as db:
                rows = db.fetchall(sql, (tournament_id,))
            return [
                Elimination(
                    elimination_id=row["elimination_id"],
                    eliminated_player_id=row["eliminated_player_id"],
                    eliminated_tournament_id=row["eliminated_tournament_id"],
                    elimination_round=row["elimination_round"],
                    position=row["position"],
                )
                for row in rows
            ]
        except Error as e:
            print(f"Database error while getting Eliminations by tournament: {e}")
            return []

    @staticmethod
    def get_by_player(player_id, tournament_id):
        sql = "SELECT * FROM Eliminations WHERE eliminated_player_id = %s AND eliminated_tournament_id = %s"
        try:
            with Database() as db:
                row = db.fetchone(sql, (player_id, tournament_id))
            if row:
                return Elimination(
                    elimination_id=row["elimination_id"],
                    eliminated_player_id=row["eliminated_player_id"],
                    eliminated_tournament_id=row["eliminated_tournament_id"],
                    elimination_round=row["elimination_round"],
                    position=row["position"],
                )
            return None
        except Error as e:
            print(
                f"Database error while getting Elimination by player and tournament: {e}"
            )
            return None
