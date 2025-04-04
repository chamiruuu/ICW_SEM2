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

def compare_cards(card1, card2):
    rank_order = Card.RANKS  # Joker has the highest index (13)
    idx1 = rank_order.index(card1.rank)
    idx2 = rank_order.index(card2.rank)
    if idx1 > idx2:
        return "Human"
    elif idx1 < idx2:
        return "PC"
    else:
        return "War"  # Tie → trigger a war
    
def handle_war(human, pc, game_log):
    war_count = 1
    while True:
        # Check if both players have at least 4 cards
        if len(human.cards) < 4 or len(pc.cards) < 4:
            return "Insufficient cards for war."
        # Draw 3 hidden + 1 visible card each
        human_drawn = [human.draw_card() for _ in range(4)]
        pc_drawn = [pc.draw_card() for _ in range(4)]
        # Compare the 4th card
        result = compare_cards(human_drawn[-1], pc_drawn[-1])
        if result != "War":
            winner = human if result == "Human" else pc
            winner.add_cards(human_drawn + pc_drawn)  # Winner takes all
            game_log.append(f"War {war_count}: {result}")
            return result
        war_count += 1  # Nested war