import sys
import random

def get_rounds():
    if len(sys.argv) == 1:  # No arguments → default to 1 round
        return 1
    elif len(sys.argv) == 2:  # Check if the second argument is valid
        try:
            rounds = int(sys.argv[1])
            if 2 <= rounds <= 5:
                return rounds
        except ValueError:
            pass  # Ignore non-integer inputs
    print("Invalid input. Using default (1 round).")
    return 1

class Card:
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', 'Joker']
    SUITS = ['♦', '♠', '♥', '♣']

    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit  # Suit is None for Jokers

    def __repr__(self):
        if self.rank == 'Joker':
            return f"{self.rank}"
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        self.cards = []
        # Generate standard cards (52)
        for suit in Card.SUITS:
            for rank in Card.RANKS[:-1]:  # Exclude Joker
                self.cards.append(Card(rank, suit))
        # Add Jokers (2)
        self.cards.append(Card('Joker'))
        self.cards.append(Card('Joker'))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def split(self):
        return self.cards[:27], self.cards[27:]  # Split into two 27-card decks
