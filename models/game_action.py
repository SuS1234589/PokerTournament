from database.db import Database
from mysql.connector import Error


class GameAction:
    def __init__(
        self,
        game_action_id=None,
        game_action_game_id=None,
        game_player_id=None,
        action_type=None,
        action_value=None,
        chips_removed=None,
    ) -> None:
        self.game_action_id = game_action_id
        self.game_action_game_id = game_action_game_id
        self.game_player_id = game_player_id
        self.action_type = action_type
        self.action_value = action_value
        self.chips_removed = chips_removed

    def __repr__(self):
        return (
            f"GameAction(id={self.game_action_id}, "
            f"game={self.game_action_game_id}, "
            f"player={self.game_player_id}, "
            f"type='{self.action_type}', "
            f"value={self.action_value}, "
            f"removed={self.chips_removed})"
        )

    @staticmethod
    def create(game_id, player_id, action_type, action_value, chips_removed):
        sql = """
        INSERT INTO GameActions (game_action_game_id, game_player_id, action_type, action_value, chips_removed)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            with Database() as db:
                db.execute(
                    sql, (game_id, player_id, action_type, action_value, chips_removed)
                )
                action_id = db.cursor.lastrowid
            return GameAction(
                game_action_id=action_id,
                game_action_game_id=game_id,
                game_player_id=player_id,
                action_type=action_type,
                action_value=action_value,
                chips_removed=chips_removed,
            )
        except Error as e:
            print(f"Database error while creating GameAction: {e}")
            return None

    @staticmethod
    def get_by_id(action_id):
        sql = "SELECT * FROM GameActions WHERE game_action_id = %s"
        try:
            with Database() as db:
                row = db.fetchone(sql, (action_id,))
            if row:
                return GameAction(
                    game_action_id=row["game_action_id"],
                    game_action_game_id=row["game_action_game_id"],
                    game_player_id=row["game_player_id"],
                    action_type=row["action_type"],
                    action_value=row["action_value"],
                    chips_removed=row["chips_removed"],
                )
            return None
        except Error as e:
            print(f"Database error while getting GameAction by ID: {e}")
            return None

    @staticmethod
    def get_by_game_id(game_id):
        sql = "SELECT * FROM GameActions WHERE game_action_game_id = %s ORDER BY game_action_id ASC"
        try:
            with Database() as db:
                rows = db.fetchall(sql, (game_id,))
            return [
                GameAction(
                    game_action_id=row["game_action_id"],
                    game_action_game_id=row["game_action_game_id"],
                    game_player_id=row["game_player_id"],
                    action_type=row["action_type"],
                    action_value=row["action_value"],
                    chips_removed=row["chips_removed"],
                )
                for row in rows
            ]
        except Error as e:
            print(f"Database error while getting GameActions by Game ID: {e}")
            return []

    def update(self):
        sql = """
        UPDATE GameActions
        SET game_action_game_id = %s, game_player_id = %s, action_type = %s, action_value = %s, chips_removed = %s
        WHERE game_action_id = %s
        """
        try:
            with Database() as db:
                db.execute(
                    sql,
                    (
                        self.game_action_game_id,
                        self.game_player_id,
                        self.action_type,
                        self.action_value,
                        self.chips_removed,
                        self.game_action_id,
                    ),
                )
                return True
        except Error as e:
            print(f"Database error while updating GameAction: {e}")
            return False
