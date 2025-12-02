import random

class Card:
    """Represents a single playing card."""
    SUITS = {'H': '♥', 'D': '♦', 'S': '♠', 'C': '♣'}
    
    def __init__(self, rank, suit_char):
        self.rank = rank
        self.suit_char = suit_char
        self.suit_symbol = self.SUITS[suit_char]
        # Red color for Hearts/Diamonds, Cyan for Spades/Clubs
        self.color = "\033[91m" if suit_char in ['H', 'D'] else "\033[96m" 
        self.reset = "\033[0m"

    def get_lines(self):
        """Returns the ASCII art lines for this specific card."""
        r = f"{self.rank:<2}" 
        s = self.suit_symbol
        c = self.color
        x = self.reset
        
        return [
            f"{c}┌─────────┐{x}",
            f"{c}│ {r}      │{x}",
            f"{c}│         │{x}",
            f"{c}│    {s}    │{x}",
            f"{c}│         │{x}",
            f"{c}│       {r}│{x}",
            f"{c}└─────────┘{x}"
        ]

class Deck:
    def __init__(self):
        ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        suits = ['H','D','S','C']
        self.cards = [Card(r, s) for r in ranks for s in suits]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop() if self.cards else None
