from database.db import Database
from mysql.connector import Error


class BlindLevel:
    def __init__(
        self,
        level_id=None,
        tournament_id=None,
        level_number=None,
        small_blind=None,
        big_blind=None,
        duration_minutes=None,
    ) -> None:
        self.level_id = level_id
        self.tournament_id = tournament_id
        self.level_number = level_number
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.duration_minutes = duration_minutes

    def __repr__(self):
        return f"Level {self.level_number} ({self.small_blind}/{self.big_blind})"

    @staticmethod
    def create_structure(tournament_id, structure):
        """
        Creates a full blind structure for a tournament from a list of dicts.
        Example structure:
        [
            {'level': 1, 'sm': 25, 'bb': 50, 'dur': 20},
            {'level': 2, 'sm': 50, 'bb': 100, 'dur': 20},
        ]
        I have no idea if this is how it should be but the working theory is this, i might just remove all of this and make it simpler
        """
        sql = """
        INSERT INTO BlindLevels (tournament_id, level_number, small_blind, big_blind, duration_minutes)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            with Database() as db:
                for level in structure:
                    db.execute(
                        sql,
                        (
                            tournament_id,
                            level["level"],
                            level["sm"],
                            level["bb"],
                            level["dur"],
                        ),
                    )
            return True
        except Error as e:
            print(f"Database error while creating BlindStructure: {e}")
            return False

    @staticmethod
    def get_by_tournament_and_level(tournament_id, level_number):
        sql = "SELECT * FROM BlindLevels WHERE tournament_id = %s AND level_number = %s"
        try:
            with Database() as db:
                row = db.fetchone(sql, (tournament_id, level_number))
            if row:
                return BlindLevel(**row)
            return None
        except Error as e:
            print(f"Database error while getting BlindLevel: {e}")
            return None
