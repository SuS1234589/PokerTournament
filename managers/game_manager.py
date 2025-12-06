from models import seating_assignment
from models import chip
from models.game import Game
from models.game_action import GameAction
from models.chip import Chip
from models.player import Player
from models.seating_assignment import SeatingAssignment
from models.elimination import Elimination

from models.cards import Deck
from deuces import Card, Evaluator

evaluator = Evaluator()

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

    deck = Deck
    hole_cards = {}
    print(f"DEALING CARD!!!!!!!!!!!!")
    for player_id, seat_number in seated_players:
        hole_cards[player_id] = [deck.deal(), deck.deal()]

    return game, seated_players, hole_cards


def run_betting_round(game: Game, players, stage, tournament_id):
    active_players = []
    highest_bet = 0
    last_raiser = None
    dealer = game.dealer_seat_number
    first_player_to_act_index = -1
    d_index = -1
    dealer_seat_number = game.dealer_seat_number
    player_bets = {}
    for i, (player_id, seat_number) in enumerate(players):
        player_bets[player_id] = 0
        active_players.append(player_id)
        if seat_number == dealer_seat_number:
            d_index = i

    num_players = len(players)

    if stage == "pre-flop" and d_index != -1:
        highest_bet = BIG_BLIND_AMOUNT
        bb_index = (d_index + 2) % num_players
        first_player_to_act_index = (bb_index + 1) % num_players

    if stage in ["flop", "turn", "river"]:
        first_player_to_act_index = -1
        for i in range(1, num_players + 1):
            checking_index = (d_index + i) % num_players
            if players[checking_index][0] in active_players:
                first_player_to_act_index = checking_index
                break
    if first_player_to_act_index == -1:
        # i think this shoudl only happen where there is only one person in the list
        return active_players

    current_player_index = first_player_to_act_index

    while True:
        current_player_id, current_player_seat_number = players[current_player_index]
        action_closed = False
        if last_raiser and current_player_id == last_raiser:
            action_closed = True
        else:
            if (
                current_player_index == first_player_to_act_index
                and last_raiser is None
            ):
                action_closed = True
        if action_closed:
            all_bets_equal = True
            for pid in active_players:
                if player_bets[pid] != highest_bet:
                    all_bets_equal = False
                    break
            if all_bets_equal:
                print("Betting round complete.")
                break

        if current_player_id not in active_players:
            current_player_index = (current_player_index + 1) % num_players
            continue

        player_chips = Chip.get_by_player_and_tournament(
            current_player_id, tournament_id
        )

        print(f"\n--- Player {current_player_id}'s Turn ---")
        print(
            f"Pot: {game.pot_amount} | "
            f"Current Bet: {highest_bet} | "
            f"Your Bet: {player_bets[current_player_id]}"
        )

        print(f"Your Chips: {player_chips.chip_balance}")

        action = input("Action (check (c), call (p), raise (r), fold (f)): ").lower()

        if action.lower() == "f" or action.lower() == "fold":
            active_players.remove(current_player_id)
            GameAction.create(game.game_id, current_player_id, "fold", 0, 0)
            print(f"Player {current_player_id} folds")

        elif action.lower() == "c" or action.lower() == "check":
            if player_bets[current_player_id] < highest_bet:
                print(
                    f"Invalid action: cannot check, there is a bet to you. Please call or raise"
                )
                continue
            else:
                GameAction.create(game.game_id, current_player_id, "check", 0, 0)
                print(f"Player {current_player_id} checks")

        elif action.lower() == "p" or action.lower() == "call":
            amount_to_bet = highest_bet - player_bets[current_player_id]
            if (
                player_chips.chip_balance <= amount_to_bet
            ):  # don't do stupid mistakes man its 3 am
                amount_to_bet = player_chips.chip_balance
                # we going all in
            player_chips.chip_balance -= amount_to_bet
            player_chips.update()

            player_bets[current_player_id] += amount_to_bet
            game.pot_amount += amount_to_bet
            game.update()

            GameAction.create(
                game.game_id,
                current_player_id,
                "call",
                player_bets[current_player_id],
                amount_to_bet,
            )
            print(f"Player{current_player_id} calls {amount_to_bet}")

        elif action.lower() == "r" or action.lower() == "raise":
            try:
                raise_amount = int(
                    input(f"Raise the amount to? Current is {highest_bet}")
                )
                if raise_amount <= highest_bet:
                    print(
                        f"Invalid amount: Raise amount must be higher than current bet: {highest_bet}"
                    )
                    continue
                amount = raise_amount - player_bets[current_player_id]
                if amount > player_chips.chip_balance:
                    print(f"You do not have enough chips for that raise")
                    continue

                player_chips.chip_balance -= amount
                player_chips.update()
                player_bets[current_player_id] += amount
                game.pot_amount += amount
                game.update()

                highest_bet = raise_amount
                last_raiser = current_player_id

                GameAction.create(
                    game.game_id, current_player_id, "raise", raise_amount, amount
                )
                print(f"Player {current_player_id} raises the bet to {raise_amount}")
            except ValueError:
                print("Invalid amount ")
                continue

        current_player_index = (current_player_index + 1) % num_players

        if len(active_players) == 1:
            break


def deal_community_cards(deck: Deck, community_list, stage):
    deck.deal()
    if stage.lower() == "flop":
        for _ in range(3):
            community_list.append(deck.deal())
    elif stage.lower() == "turn" or stage.lower() == "river":
        community_list.append(deck.deal())
    else:
        print(f"Unkown stage")
    return community_list


def determine_winner(game, active_players, hole_cards, community_cards):
    best_score = float("inf")
    winners = []
    community_deuces = []
    for card in community_cards:
        rank_string = "T" if card.rank == "10" else card.rank
        card_string_d = rank_string + card.suit_char.lower()
        community_deuces.append(Card.new(card_string_d))

    print(f"\n---SHOWDOWN---")  # i wanna sleep what is this deuce

    for player_id in active_players:
        player_hole_cards = hole_cards[player_id]

        hole_d = []
        for card in player_hole_cards:
            rank_string = "T" if card.rank == "10" else card.rank
            card_string_d = rank_string + card.suit_char.lower()
            hole_d.append(Card.new(card_string_d))

        # lower the score the better, remember that!
        score = evaluator.evaluate(hole_d + community_deuces)
        # yo this thing is cool as hell
        rank_class = evaluator.get_rank_class(score)
        rank_name = evaluator.class_to_string(rank_class)

        hold_card_string = [str(i) for i in player_hole_cards]
        print(
            f"Player {player_id} shows {hold_card_string} for a {rank_name} Score:{score}"
        )
        if score < best_score:
            best_score = score
            # only winner, chicken dinnner
            winners = [player_id]
        elif score == best_score:
            # not the only winner, no dinnner
            winners.append(player_id)
    rank_class = evaluator.get_rank_class(best_score)
    rank_name = evaluator.class_to_string(rank_class)

    print(f" Winner: {winners} with a {rank_name}! ")
    return winners


def check_for_eliminations(table_id):
    # get them out of the tournament heheheheheheeh
    all_players = SeatingAssignment.get_by_table(table_id)

    if not all_players:
        return 

    for player in all_players:
        chips = Chip.get_by_player_and_tournament(
            player.player_id, player.tournament_id
        )
        if chips.chip_balance == 0:
            player_from_player = Player.get_by_id(player.player_id) # what a shitty variable namen 
            if player_from_player:
                player_from_player.status = "eliminated"
                player_from_player.update()  # DON't MAKE MISTAKES DON't FORGET TO UPDATE
            # i actually have no idea how to track position and stuff and i do not wanna thihnk about it i might just remove it later, until unless lucas decides he wanna do leaderboard, then its his problem, for now 0 is a placeholder
            Elimination.create(player.player_id, player.tournament_id, 1, 0)
