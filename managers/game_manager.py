from models import seating_assignment
from models import chip
from models.game import Game
from models.game_action import GameAction
from models.chip import Chip
from models.seating_assignment import SeatingAssignment
from models.elimination import Elimination

from models.cards import Deck

SMALL_BLIND_AMOUNT = 25
BIG_BLIND_AMOUNT = 50


def run_full_hand(tournament_id, table_id):
    pass


def start_new_hand(tournament_id, table_id):
    initial_pot = 0
    players_on_table = SeatingAssignment.get_by_table(table_id)
    if not players_on_table or len(players_on_table) < 2:
        print(f"Error not enough players or something like that in game_manager.py")
        return None, [], {}

    seated_players = [(row.player_id, row.seat_number) for row in players_on_table]
    num_players = len(seated_players)

    seated_players.sort(key=lambda x: x[1])
    last_game = Game.get_last_hand_for_table(table_id)

    if last_game:
        last_dealer_index = -1
        for i, (player_id, seat_number) in enumerate(seated_players):
            if seat_number == last_game.dealer_seat_number:
                last_dealer_index = i
                break
        if last_dealer_index != -1:
            new_dealer_index = (last_dealer_index + 1) % num_players
        else:
            new_dealer_index = random.randrange(num_players)

    else:
        new_dealer_index = random.randrange(num_players)

    new_dealer_player_id, new_dealer_seat_number = seated_players[new_dealer_index]
    if last_game:
        new_hand_number = last_game.hand_number + 1
    else:
        new_hand_number = 1

    game = Game.create(tournament_id, table_id, new_hand_number, new_dealer_seat_number)
    if not game:
        print(f"Error: Failed to create a new game record.")
        return None, [], {}

    print(f"\n---Starting Hand #{new_hand_number} at Table {table_id}")
    print(f"Dealer is player {new_dealer_player_id} in seat {new_dealer_seat_number}")

    if num_players == 2:
        small_bid_index = new_dealer_index
        big_bid_index = (new_dealer_index + 1) % num_players
    else:
        small_bid_index = (new_dealer_index + 1) % num_players
        big_bid_index = (new_dealer_index + 2) % num_players

    # small_bd
    small_bid_player_id, small_bid_seat_number = seated_players[small_bid_index]
    small_bid_chips = Chip.get_by_player_and_tournament(
        small_bid_player_id, tournament_id
    )
    if small_bid_chips and small_bid_chips.chip_balance > 0:
        chips_posted = min(SMALL_BLIND_AMOUNT, small_bid_chips.chip_balance)
        small_bid_chips.chip_balance -= chips_posted
        small_bid_chips.update()
        initial_pot += chips_posted
        GameAction.create(
            game.game_id,
            small_bid_player_id,
            "small_blind",
            chips_posted,
            chips_posted,
        )
        print(
            f"Player {small_bid_player_id} (seat {small_bid_seat_number}) posts small blind of {chips_posted}"
        )

    big_bid_player_id, big_bid_seat_number = seated_players[big_bid_index]
    big_bid_chips = Chip.get_by_player_and_tournament(big_bid_player_id, tournament_id)
    if big_bid_chips and big_bid_chips.chip_balance > 0:
        chips_posted = min(BIG_BLIND_AMOUNT, big_bid_chips.chip_balance)
        big_bid_chips.chip_balance -= chips_posted
        big_bid_chips.update()
        initial_pot += chips_posted
        GameAction.create(
            game.game_id, big_bid_player_id, "big_blind", chips_posted, chips_posted
        )
        print(
            f"Player {big_bid_player_id} (seat {big_bid_seat_number}) posts big blind of {chips_posted}"
        )

    game.pot_amount = initial_pot
    game.update()

    deck = Deck()
    hole_cards = {}
    print(f"DEALING CARD!!!!!!!!!!!!")
    for player_id, seat_number in seated_players:
        hole_cards[player_id] = [deck.deal(), deck.deal()]

    return game, seated_players, hole_cards


def run_betting_round(game, players, stage):
    pass


def deal_community_cards(stage):
    pass


def determine_winner(game, active_players, hole_cards, community_cards):
    pass


def check_for_eliminations(table_id):
    pass
