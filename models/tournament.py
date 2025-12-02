from database.db import Database
from mysql.connector import Error


class Tournament:
    def __init__(
        self, tournament_id=None, name=None, description=None, organizer_id=None
    ) -> None:
        self.tournament_id = tournament_id
        self.name = name
        self.description = description
        self.organizer_id = organizer_id

    def __repr__(self):
        return f"Tournament(id={self.tournament_id}, name='{self.name}')"

    @staticmethod
    def create(name, description, organizer_id):
        sql = """
        INSERT INTO Tournaments (name, Description, organizer_id)
        VALUES (%s,%s,%s)
        """
        try:
            with Database() as db:
                db.execute(sql, (name, description, organizer_id))
                tournament_id = db.cursor.lastrowid
            return Tournament(
                tournament_id=tournament_id,
                name=name,
                description=description,
                organizer_id=organizer_id,
            )

        except Error as e:
            print(f"Database error while creating Tournament: {e}")
            return False

    @staticmethod
    def get_by_id(tournament_id):
        sql = "SELECT * FROM Tournaments WHERE tournament_id = %s"
        try:
            with Database() as db:
                row = db.fetchone(sql, (tournament_id,))
            if row:
                return Tournament(
                    tournament_id=row['tournament_id'],
                    name=row['name'],
                    description=row['Description'],
                    organizer_id=row['organizer_id']
                )
        except Error as e:
            print(f"Database error while getting tournament by ID: {e}")
            return None

    @staticmethod
    def get_all():
        sql = "SELECT * FROM Tournaments"
        try:
            with Database() as db:
                rows = db.fetchall(sql)
            return [
                Tournament(
                    tournament_id=row['tournament_id'],
                    name=row['name'],
                    description=row['Description'],
                    organizer_id=row['organizer_id']
                ) for row in rows
            ]
        except Error as e:
            print(f"Database error while getting all Tournaments: {e}")
            return []

    def update(self):
        sql = """
        UPDATE Tournaments
        SET name = %s, Description = %s, organizer_id = %s
        WHERE tournament_id = %s
        """
        try:
            with Database() as db:
                db.execute(
                    sql,
                    (
                        self.name,
                        self.description,
                        self.organizer_id,
                        self.tournament_id,
                    ),
                )
                return True
        except Error as e:
            print(f"Database error while updating Tournament: {e}")
            return False

    def delete(self):
        sql = "DELETE FROM Tournaments WHERE tournament_id = %s"
        try:
            with Database() as db:
                db.execute(sql, (self.tournament_id,))
                return True
        except Error as e:
            print(f"Database error while deleting the Tournament: {e}")
            return False