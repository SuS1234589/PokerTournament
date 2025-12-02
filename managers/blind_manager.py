import datetime
from models.tournament import Tournament
from models.blind_level import BlindLevel


def start_blind_timer(tournament_id):
    """
    Starts the blind timer for a tournament.
    Sets the current level to 1 and records the start time.
    """
    tourn = Tournament.get_by_id(tournament_id)
    if not tourn:
        print("Tournament not found.")
        return

    tourn.current_blind_level = 1
    tourn.level_start_time = datetime.datetime.now()
    if tourn.update():
        print(f"Tournament {tourn.name} started. Blinds at level 1.")
    else:
        print("Failed to start tournament timer.")


def advance_blind_level(tournament_id):
    """
    Manually advances the tournament to the next blind level.
    """
    tourn = Tournament.get_by_id(tournament_id)
    if not tourn:
        print("Tournament not found.")
        return

    next_level = (tourn.current_blind_level or 0) + 1
    
    # Check if the next level exists
    blind_level = BlindLevel.get_by_tournament_and_level(tournament_id, next_level)
    if not blind_level:
        print("End of blind structure reached. Cannot advance.")
        return

    tourn.current_blind_level = next_level
    tourn.level_start_time = datetime.datetime.now()
    if tourn.update():
        print(f"Blinds advanced to Level {blind_level.level_number}: {blind_level.small_blind}/{blind_level.big_blind}")
    else:
        print("Failed to advance blind level.")


def check_blinds(tournament_id):
    """
    Checks the current blind level and time remaining.
    Advances the level automatically if the time has expired.
    """
    tourn = Tournament.get_by_id(tournament_id)
    if not tourn or not tourn.current_blind_level or not tourn.level_start_time:
        print("Tournament is not active or timer has not been started.")
        return

    blind_level = BlindLevel.get_by_tournament_and_level(
        tournament_id, tourn.current_blind_level
    )
    if not blind_level:
        print(f"Could not find details for blind level {tourn.current_blind_level}.")
        return

    elapsed_time = datetime.datetime.now() - tourn.level_start_time
    duration = datetime.timedelta(minutes=blind_level.duration_minutes)
    time_remaining = duration - elapsed_time

    print(f"--- Current Blinds (Level {blind_level.level_number}) ---")
    print(f"Blinds: {blind_level.small_blind}/{blind_level.big_blind}")

    if time_remaining.total_seconds() > 0:
        # Format to M:SS
        minutes, seconds = divmod(int(time_remaining.total_seconds()), 60)
        print(f"Time Remaining: {minutes:02d}:{seconds:02d}")
    else:
        print("Time has expired for this level. Advancing...")
        advance_blind_level(tournament_id)
    
    print("-------------------------")
