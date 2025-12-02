from database.db import Database
from mysql.connector import Error
from models.table import Table


class SeatingAssignment:
    def __init__(
        self,
        seat_id=None,
        tournament_id=None,
        table_id=None,
        player_id=None,
        seat_number=None,
    ) -> None:
        self.seat_id = seat_id
        self.tournament_id = tournament_id
        self.table_id = table_id
        self.player_id = player_id
        self.seat_number = seat_number

    def __repr__(self):
        return (
            f"Seat(id={self.seat_id}, "
            f"tournament={self.tournament_id}, "
            f"table={self.table_id}, "
            f"player={self.player_id}, "
            f"seat_number={self.seat_number})"
        )

    @staticmethod
    def create(tour_id, tab_id, player_id):
        sql = "SELECT seat_number FROM SeatingAssignment WHERE table_id = %s AND tournament_id = %s"
        try:
            with Database() as db:
                existing_rows = db.fetchall(sql, (tab_id, tour_id))
        except Error as e:
            print(f"Database error while getting existing from seating assignment: {e}")
            return None

        existing_seats = {row["seat_number"] for row in existing_rows}
        seat_number = 0
        max_seats = Table.get_max_seats(tour_id, tab_id)
        if max_seats is None:
            print(
                f"Could not determine max seats for table {tab_id} in tournament {tour_id}"
            )
            return None

        for i in range(1, max_seats + 1):
            if i not in existing_seats:
                seat_number = i
                break

        if seat_number == 0:
            print(f"No available seats at table {tab_id} in tournament {tour_id}")
            return None

        sql = """
        INSERT INTO SeatingAssignment(tournament_id, table_id, player_id, seat_number)
        VALUES(%s, %s, %s, %s)
        """
        try:
            with Database() as db:
                db.execute(sql, (tour_id, tab_id, player_id, seat_number))
                seat_id = db.cursor.lastrowid
            return SeatingAssignment(
                seat_id=seat_id,
                tournament_id=tour_id,
                table_id=tab_id,
                player_id=player_id,
                seat_number=seat_number,
            )
        except Error as e:
            print(f"Database error while creating SeatingAssignment: {e}")
            return None

    @staticmethod
    def get_by_player(player_id):
        sql = "SELECT * FROM SeatingAssignment WHERE player_id = %s"
        try:
            with Database() as db:
                rows = db.fetchall(sql, (player_id,))
            return [
                SeatingAssignment(
                    seat_id=row["seat_id"],
                    tournament_id=row["tournament_id"],
                    table_id=row["table_id"],
                    player_id=row["player_id"],
                    seat_number=row["seat_number"],
                )
                for row in rows
            ]
        except Error as e:
            print(f"Database error while getting SeatingAssignment by player: {e}")
            return []

    @staticmethod
    def get_by_tournament(tournament_id):
        sql = "SELECT * FROM SeatingAssignment WHERE tournament_id = %s"
        try:
            with Database() as db:
                rows = db.fetchall(sql, (tournament_id,))
            return [
                SeatingAssignment(
                    seat_id=row["seat_id"],
                    tournament_id=row["tournament_id"],
                    table_id=row["table_id"],
                    player_id=row["player_id"],
                    seat_number=row["seat_number"],
                )
                for row in rows
            ]
        except Error as e:
            print(f"Database error while getting SeatingAssignment by tournament: {e}")
            return []

    @staticmethod
    def get_by_table(table_id):
        sql = "SELECT * FROM SeatingAssignment WHERE table_id = %s"
        try:
            with Database() as db:
                rows = db.fetchall(sql, (table_id,))
            return [
                SeatingAssignment(
                    seat_id=row["seat_id"],
                    tournament_id=row["tournament_id"],
                    table_id=row["table_id"],
                    player_id=row["player_id"],
                    seat_number=row["seat_number"],
                )
                for row in rows
            ]
        except Error as e:
            print(f"Database error while getting SeatingAssignment by table: {e}")
            return []

    def delete(self):
        sql = "DELETE FROM SeatingAssignment WHERE seat_id = %s"
        try:
            with Database() as db:
                db.execute(sql, (self.seat_id,))
                return True
        except Error as e:
            print(f"Database error while deleting SeatingAssignment: {e}")
            return False
