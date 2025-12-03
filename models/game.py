from database.db import Database
from mysql.connector import Error


class Game:
    def __init__(
        self,
        game_id=None,
        game_tournament_id=None,
        game_table_id=None,
        hand_number=None,
        dealer_seat_number=None,
        pot_amount=None,
    ) -> None:
        self.game_id = game_id
        self.game_tournament_id = game_tournament_id
        self.game_table_id = game_table_id
        self.hand_number = hand_number
        self.dealer_seat_number = dealer_seat_number
        self.pot_amount = pot_amount

    @staticmethod
    def create(tour_id, tab_id, hand_number, dealer_seat_number):
        sql = """
        INSERT INTO Games(game_tournament_id, game_table_id, hand_number, dealer_seat_number, pot_amount)
        VALUES(%s,%s,%s,%s,%s)
        """
        try:
            with Database() as db:
                pot_amount = 0  # ! THIS NEED TO BE CHANGED, I THINK THERE WAS SOMETHING LIKE WE HAVE TO USE THE VALUE OF THE BLINDS
                db.execute(
                    sql, (tour_id, tab_id, hand_number, dealer_seat_number, pot_amount)
                )
                game_id = db.cursor.lastrowid

            return Game(
                game_id=game_id,
                game_tournament_id=tour_id,
                game_table_id=tab_id,
                hand_number=hand_number,
                dealer_seat_number=dealer_seat_number,
                pot_amount=pot_amount,
            )
        except Error as e:
            print(f"Database error while inseting game: {e}")
            return False

    @staticmethod
    def get_by_id(game_id):
        sql = "SELECT * FROM Games WHERE game_id = %s"
        try:
            with Database() as db:
                row = db.fetchone(sql, (game_id,))
            if row:
                return Game(
                    game_id=row["game_id"],
                    game_tournament_id=row["game_tournament_id"],
                    game_table_id=row["game_table_id"],
                    hand_number=row["hand_number"],
                    dealer_seat_number=row["dealer_seat_number"],
                    pot_amount=row["pot_amount"],
                )
            return None
        except Error as e:
            print(f"Database error while fetching by id: {e}")
            return None

    def update(self):
        sql = """
        UPDATE Games 
        SET dealer_seat_number = %s, hand_number = %s, pot_amount = %s WHERE game_id = %s
        """
        try:
            with Database() as db:
                db.execute(
                    sql,
                    (
                        self.dealer_seat_number,
                        self.hand_number,
                        self.pot_amount,
                        self.game_id,
                    ),
                )
                return True
        except Error as e:
            print(f"Databae error while updating Game: {e}")
            return False
