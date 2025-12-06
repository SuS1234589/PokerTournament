import time
import os
from .cards import Deck


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_hand(cards, label=None):
    if label:
        print(f"\n{label}")

    if not cards:
        return

    lines_per_card = [card.get_lines() for card in cards]

    for i in range(7):
        print("  ".join(line[i] for line in lines_per_card))


def run_poker_simulation():
    clear_screen()
    # add logic for table/tournament names later
    print("--- JOINING TABLE: ---")
    deck = Deck()
    print("Dealer is shuffling...", end="", flush=True)
    time.sleep(1)
    print(" Done.")

    # 1. Deal Hole Cards
    hero_hand = [deck.deal(), deck.deal()]
    print_hand(hero_hand, label="[Your Hand]")
    input("\n[Action] Press Enter to see the Flop...")

    # 2. The Flop
    board = [deck.deal(), deck.deal(), deck.deal()]
    print_hand(board, label="[The Flop]")
    # Reprint user hand so they don't lose track
    print_hand(hero_hand, label="[Your Hand]")
    input("\n[Action] Press Enter to see the Turn...")

    # 3. The Turn
    board.append(deck.deal())
    print_hand(board, label="[The Turn]")
    # Reprint user hand so they don't lose track
    print_hand(hero_hand, label="[Your Hand]")
    input("\n[Action] Press Enter to see the River...")

    # 4. The River
    board.append(deck.deal())
    print_hand(board, label="[The River]")
    # Reprint user hand so they don't lose track
    print_hand(hero_hand, label="[Your Hand]")

    # End
    print("\n--- Hand Complete ---")
    input("[Action] Press Enter to leave the table...")
