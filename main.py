import sys
import random
import datetime
import os

def create_deck():
    """Create a deck of cards including Jokers."""
    suits = ['♥', '♦', '♣', '♠']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [{'rank': value, 'suit': suit} for suit in suits for value in values]
    deck.append({'rank': 'Joker', 'suit': '♥'})
    deck.append({'rank': 'Joker', 'suit': '♠'})
    return deck

def shuffle_deck(deck):
    """Shuffle the deck of cards."""
    random.shuffle(deck)

def deal_cards(deck, num_players=2):
    """Deal cards evenly to players."""
    hands = [[] for _ in range(num_players)]
    for i, card in enumerate(deck):
        hands[i % num_players].append(card)
    return hands

def card_value(card):
    """Get the numeric value of a card."""
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', 'Joker']
    return values.index(card['rank'])

def play_round(human_cards, pc_cards, round_num, game_history):
    """Play a single round of the game."""
    print(f"=== Round {round_num} ===")
    play_count = 0
    human_pile = []
    pc_pile = []

    while play_count < 27 and human_cards and pc_cards:
        play_count += 1
        human_card = human_cards.pop(0)
        pc_card = pc_cards.pop(0)

        print(f"Play {play_count}: Human plays {human_card['rank']}{human_card.get('suit', '')} - PC plays {pc_card['rank']}{pc_card.get('suit', '')}")

        if card_value(human_card) > card_value(pc_card):
            winner = "Human"
            human_pile.extend([human_card, pc_card])
            print(f"{winner} wins this play")
        elif card_value(pc_card) > card_value(human_card):
            winner = "PC"
            pc_pile.extend([human_card, pc_card])
            print(f"{winner} wins this play")
        else:
            print("WAR! Both cards are equal")
            winner, war_cards = handle_war(human_cards, pc_cards, human_card, pc_card)
            if winner == "Human":
                human_pile.extend(war_cards)
            else:
                pc_pile.extend(war_cards)

        game_history.append({
            'round': round_num,
            'play_num': play_count,
            'human_card': f"{human_card['rank']}{human_card.get('suit', '')}",
            'pc_card': f"{pc_card['rank']}{pc_card.get('suit', '')}",
            'winner': winner
        })

    return human_pile, pc_pile

def handle_war(human_cards, pc_cards, human_card, pc_card):
    """Handle a war situation."""
    print("Drawing 3 hidden cards and 1 visible card...")
    war_cards = [human_card, pc_card]

    if len(human_cards) < 4 or len(pc_cards) < 4:
        print("Not enough cards for war. Game ends.")
        return "PC" if len(human_cards) < 4 else "Human", war_cards

    human_war_cards = [human_cards.pop(0) for _ in range(3)]
    pc_war_cards = [pc_cards.pop(0) for _ in range(3)]
    human_war_card = human_cards.pop(0)
    pc_war_card = pc_cards.pop(0)

    war_cards.extend(human_war_cards + pc_war_cards + [human_war_card, pc_war_card])

    print(f"War cards revealed: Human plays {human_war_card['rank']}{human_war_card.get('suit', '')} - PC plays {pc_war_card['rank']}{pc_war_card.get('suit', '')}")

    if card_value(human_war_card) > card_value(pc_war_card):
        print("Human wins the war!")
        return "Human", war_cards
    elif card_value(pc_war_card) > card_value(human_war_card):
        print("PC wins the war!")
        return "PC", war_cards
    else:
        print("Another war!")
        return handle_war(human_cards, pc_cards, human_war_card, pc_war_card)

def determine_winner(human_pile, pc_pile):
    """Determine the winner of the game."""
    human_total = len(human_pile)
    pc_total = len(pc_pile)

    print("\n=== FINAL RESULT ===")
    print(f"Human cards: {human_total}")
    print(f"PC cards: {pc_total}")

    if human_total > pc_total:
        return "Human"
    elif pc_total > human_total:
        return "PC"
    else:
        return "Tie"

def save_game_history(game_history, winner):
    """Save the game history to both a text file and an HTML file."""
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d_%H%M%S')
    txt_filename = f"war_game_{timestamp}.txt"
    html_filename = f"war_game_{timestamp}.html"

    # Save to text file
    with open(txt_filename, 'w') as txt_file:
        txt_file.write("=== GAME HISTORY ===\n")
        for entry in game_history:
            txt_file.write(f"Round {entry['round']} - Play {entry['play_num']}: {entry['human_card']} vs {entry['pc_card']} - Winner: {entry['winner']}\n")
        txt_file.write(f"\nWinner: {winner}\n")

    print(f"Game history saved to {txt_filename}")

    # Save to HTML file
    with open(html_filename, 'w') as html_file:
        html_file.write("<!DOCTYPE html>\n")
        html_file.write("<html lang='en'>\n")
        html_file.write("<head>\n")
        html_file.write("<meta charset='UTF-8'>\n")
        html_file.write("<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
        html_file.write(f"<title>War Game History - {timestamp}</title>\n")
        html_file.write("</head>\n")
        html_file.write("<body>\n")
        html_file.write("<h1>Game History</h1>\n")
        html_file.write("<table border='1'>\n")
        html_file.write("<tr><th>Round</th><th>Play</th><th>Human Card</th><th>PC Card</th><th>Winner</th></tr>\n")
        for entry in game_history:
            html_file.write(f"<tr><td>{entry['round']}</td><td>{entry['play_num']}</td><td>{entry['human_card']}</td><td>{entry['pc_card']}</td><td>{entry['winner']}</td></tr>\n")
        html_file.write("</table>\n")
        html_file.write(f"<h2>Winner: {winner}</h2>\n")
        html_file.write("</body>\n")
        html_file.write("</html>\n")

    print(f"Game history saved to {html_filename}")

def play_game(rounds=1):
    """Play the War card game."""
    deck = create_deck()
    shuffle_deck(deck)
    hands = deal_cards(deck)
    human_cards, pc_cards = hands

    game_history = []
    for round_num in range(1, rounds + 1):
        human_pile, pc_pile = play_round(human_cards, pc_cards, round_num, game_history)
        human_cards.extend(human_pile)
        pc_cards.extend(pc_pile)
        shuffle_deck(human_cards)
        shuffle_deck(pc_cards)

    winner = determine_winner(human_cards, pc_cards)
    save_game_history(game_history, winner)

def main():
    """Main function to start the game."""
    rounds = 1
    if len(sys.argv) > 1:
        try:
            rounds = int(sys.argv[1])
            if not 1 <= rounds <= 5:
                print("Number of rounds must be between 1 and 5.")
                rounds = 1
        except ValueError:
            print("Invalid input. Defaulting to 1 round.")
    play_game(rounds)

if __name__ == "__main__":
    main()