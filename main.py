import random  # For shuffling the deck
import datetime  # For generating unique filenames

# Constants for card suits and ranks
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14, 'Joker': 15  # Jokers are the highest
}

# Function to create a full deck of cards (52 + 2 Jokers)
def create_deck():
    deck = []
    
    # Add standard 52 cards
    for suit in SUITS:
        for rank, value in RANKS.items():
            if rank != 'Joker':  # Avoid adding Joker in the main loop
                deck.append((rank, suit, value))  # Tuple: (Rank, Suit, Value)

    # Add two Jokers (without a suit)
    deck.append(('Joker', 'Red', RANKS['Joker']))
    deck.append(('Joker', 'Black', RANKS['Joker']))

    return deck

# Function to shuffle and distribute cards equally between player and computer
def shuffle_and_distribute(deck):
    random.shuffle(deck)  # Shuffle the deck
    mid = len(deck) // 2  # Split the deck into two
    return deck[:mid], deck[mid:]

# Entry point of the game
def main():
    print("Welcome to the War Card Game!")

    # Step 1: Create and shuffle the deck
    deck = create_deck()
    player_deck, computer_deck = shuffle_and_distribute(deck)

    # Display the number of cards each player has
    print(f"Deck shuffled! Each player has {len(player_deck)} cards.")

if __name__ == "__main__":
    main()