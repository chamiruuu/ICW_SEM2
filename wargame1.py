import random
import sys
import os
from datetime import datetime

def create_deck():
    #create the card values for deck
    suits = ['♠', '♥', '♦', '♣']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = []
    for suit in suits:
        for value in values:
            deck.append({'value': value, 'suit': suit})  
    # Add 2 jokers
    deck.append({'value': 'Joker', 'suit': '♥'})
    deck.append({'value': 'Joker', 'suit': '♠'})
    return deck

def shuffle_deck(deck):
    # Shuffle the deck using random.shuffle
    random.shuffle(deck)
    return deck

def compare_cards(cd1, cd2):
    #*Compare two cards based on their values"""
    # Joker is the highest card, followed by Ace, then 2-10, J, Q, K
    values_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', 'Joker']
    return values_order.index(cd1['value']) - values_order.index(cd2['value'])

def distribute_cards(deck):
    return deck[:27], deck[27:54]#* Distribute the deck into two equal parts for human and PC"""

def handle_war(human_deck, pc_deck, war_pile, battles):
    # Add the first 3 face-down cards from each player
    for _ in range(3):
        # Check if either player doesn't have enough cards for war
        if not human_deck or not pc_deck:
            # Determine winner based on remaining cards
            winner = "H" if len(human_deck) > len(pc_deck) else "P"
            return winner, war_pile + human_deck + pc_deck, battles
        h_card = human_deck.pop(0)
        p_card = pc_deck.pop(0)
        war_pile.extend([h_card, p_card])
        battles.append((h_card, p_card, "WAR-DOWN"))
    
    if not human_deck or not pc_deck:    # Fourth card is face-up for comparison
        # If either player runs out of cards before the 4th card
        winner = "H" if len(human_deck) > len(pc_deck) else "P"
        return winner, war_pile, battles
    
    h_card = human_deck.pop(0)
    p_card = pc_deck.pop(0)
    war_pile.extend([h_card, p_card])
    battles.append((h_card, p_card, "WAR-UP"))  # Record the face-up war cards
    result = compare_cards(h_card, p_card)  # Compare the 4th cards
    
    if result > 0:  # Human wins
        return "H", war_pile, battles
    elif result < 0:  # PC wins
        return "P", war_pile, battles
    else:  # Another war - continue recursively
        return handle_war(human_deck, pc_deck, war_pile, battles)

def play_game(rounds=1):  # Play the War card game for a specified number of rounds
    # Create and shuffle the deck
    deck = create_deck()
    shuffled_deck = shuffle_deck(deck)
    all_battles = []
    round_results = []
    
    # Play the specified number of rounds
    for round_num in range(1, rounds + 1):
        # Re-shuffle and distribute cards at the start of each round
        shuffled_deck = shuffle_deck(shuffled_deck)
        human_deck, pc_deck = distribute_cards(shuffled_deck)
        human_won = []
        pc_won = []
        wars = 0
        battles = []
        max_plays = 27  # Each player has 27 cards
        play_count = 0
        while human_deck and pc_deck and play_count < max_plays:
            play_count += 1
            h_card = human_deck.pop(0)  # Each player draws one card
            p_card = pc_deck.pop(0)
            result = compare_cards(h_card, p_card)  # Compare cards (ignoring suits)
            if result > 0:  # Human wins
                human_won.extend([h_card, p_card])
                battles.append((h_card, p_card, "H"))
            elif result < 0:  # PC wins
                pc_won.extend([h_card, p_card])
                battles.append((h_card, p_card, "P"))
            else:  # War - same value cards
                wars += 1
                battles.append((h_card, p_card, "WAR"))
                war_pile = [h_card, p_card]# Start war with the tied cards
                war_winner, won_cards, war_battles = handle_war(human_deck, pc_deck, war_pile, [])
                battles.extend(war_battles)# Add the war battles to our battle history
                if war_winner == "H":
                    human_won.extend(won_cards)
                elif war_winner == "P":
                    pc_won.extend(won_cards)
                # If either player ran out of cards during war
                if not human_deck or not pc_deck:
                    break
        # Determine round winner based on card count
        h_total = len(human_won)
        p_total = len(pc_won)
        round_winner = "PC" if p_total > h_total else "Human" if h_total > p_total else "Tie"
        round_results.append({
            'round': round_num,
            'human': h_total,
            'pc': p_total,
            'wars': wars,
            'winner': round_winner
        })
        
        all_battles.append(battles)
        if round_num < rounds:# Update the deck for next round if multiple rounds are being played
            shuffled_deck = shuffle_deck(human_won + pc_won)
    last_round = round_results[-1]# Determine the overall winner based on the last round
    h_final = last_round['human']
    p_final = last_round['pc']
    winner = "PC won the game!" if p_final > h_final else \
             "Human won the game!" if h_final > p_final else \
             "The game is a tie!"
    total_wars = sum(r['wars'] for r in round_results)
    return {
        'rounds': rounds,
        'human': h_final,
        'pc': p_final,
        'wars': total_wars,
        'winner': winner,
        'round_results': round_results,
        'all_battles': all_battles
    }

def format_game_output(results):#* Format the game results for output"""
    now = datetime.now()
    output = []
    output.append(f"Date : {now.strftime('%Y-%m-%d')}")
    output.append(f"Time : {now.strftime('%H:%M')}")
    output.append("")
    output.append(f"Total Rounds : {results['rounds']}")
    output.append("")
    for round_num, battles in enumerate(results['all_battles'], 1):
        output.append(f"Round {round_num} results")
        output.append("-------------------------")
        output.append("No : Hum vs PC - Winner")
        battle_count = 0
        for i, (h_card, p_card, winner) in enumerate(battles, 1):
            # Skip face-down war cards in the simplified output format
            if winner == "WAR-DOWN":
                continue
            battle_count += 1
            h = f"{h_card['value']}{h_card['suit']}"
            p = f"{p_card['value']}{p_card['suit']}"
            # Format according to the image example
            winner_display = winner
            if winner == "WAR-UP":
                winner_display = "WAR"
            output.append(f"{battle_count} : {h} vs {p} - {winner_display}")
        output.append("")
    
    # Final results - matching image format exactly
    output.append(f"PC card count {results['pc']}")
    output.append(f"Human card count {results['human']}")
    output.append(f"War count {results['wars']}")
    output.append("")
    output.append(f"{results['winner']}")
    return "\n".join(output)
def save_text_results(results, unique_id):#*Save results as text file with formatted output"""
    filename = f"war_{unique_id}.txt"
    formatted_output = format_game_output(results)# Get the formatted output

    with open(filename, 'w', encoding='utf-8') as f:    # Write to file
        f.write(formatted_output)
    return filename

def save_html_results(results, unique_id):#* Save results as HTML file with formatted output"""
    now = datetime.now()
    filename = f"war_{unique_id}.html"
    
    # Start building HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>War Card Game - {now.strftime('%Y-%m-%d')}</title>
    <style>
      
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            white-space: pre;
        }}
        .hearts, .diamonds {{
            color: red;
        }}
        .war {{
            font-weight: bold;
        }}
        .winner {{
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
Date : {now.strftime('%Y-%m-%d')}
Time : {now.strftime('%H:%M')}

Total Rounds : {results['rounds']}

"""
    
    # Add round results
    for round_num, battles in enumerate(results['all_battles'], 1):
        html_content += f"""Round {round_num} results
-------------------------
No : Hum vs PC - Winner
"""
        
        battle_count = 0
        for i, (h_card, p_card, winner) in enumerate(battles, 1):
            # Skip face-down war cards in the output
            if winner == "WAR-DOWN":
                continue
                
            battle_count += 1
            
            # Format cards with color based on suit
            h_colored = style_card_html(h_card)
            p_colored = style_card_html(p_card)
            
            # Format winner
            winner_display = winner
            if winner == "WAR-UP":
                winner_display = '<span class="war">WAR</span>'
            
            html_content += f"""{battle_count} : {h_colored} vs {p_colored} - {winner_display}
"""
        html_content += """\n\n\n
""" 
    html_content += f"""PC card count {results['pc']}   
Human card count {results['human']}
War count {results['wars']}
<span class="winner">{results['winner']}</span>
"""  
    html_content += """    </div>
</body>
</html>""" # Close HTML tags

    with open(filename, 'w', encoding='utf-8') as f:    # Write HTML file
        f.write(html_content)
    return filename
def style_card_html(card):
    """Apply styling to cards based on suit for HTML output"""
    card_str = f"{card['value']}{card['suit']}"
    
    if card['suit'] == '♥' or card['suit'] == '♦':
        return f'<span class="hearts">{card_str}</span>'
    return card_str

def parse_command_line():#* Parse command line arguments for number of rounds"""
    rounds = 1# Default values
    # Check for command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        # Check for both formats: with and without space
        if arg in ["war", "war1", "war 1"]:
            rounds = 1
        elif arg in ["war2", "war 2"]:
            rounds = 2
        elif arg in ["war3", "war 3"]:
            rounds = 3
        elif arg in ["war4", "war 4"]:
            rounds = 4
        elif arg in ["war5", "war 5"]:
            rounds = 5
        elif arg.isdigit():
            # If just a number is passed
            rounds = min(max(1, int(arg)), 5)
        else:
            print("Invalid input. Using default (1 round).")
    return rounds

def main():#* Main function to run the War card game"""
    print("\n    WAR game    ")
    rounds = parse_command_line()    # Get number of rounds from command line
    if len(sys.argv) <= 1:   # Allow user to input from keyboard if no command line args
        try:
            user_input = input("Enter 'War' followed by a number (1-5) to start the game: ").strip().lower()           
            # Check for both formats: with and without space
            if user_input in ["war", "war1", "war 1"]:
                rounds = 1
            elif user_input in ["war2", "war 2"]:
                rounds = 2
            elif user_input in ["war3", "war 3"]:
                rounds = 3
            elif user_input in ["war4", "war 4"]:
                rounds = 4
            elif user_input in ["war5", "war 5"]:
                rounds = 5
            else:
                print("Invalid input. Using default (1 round).")
        except Exception as e:
            print(f"Error with input: {e}")
            print("Using default (1 round).")
    
    print(f"\nStarting War game ({rounds} round{'s' if rounds > 1 else ''})...")
    game = play_game(rounds)  # Play the game
    unique_id = f"{datetime.now().strftime('%Y%m%d%H%M')}_{random.randint(1000, 9999)}"  # Generate a unique ID for the files
    text_file = save_text_results(game, unique_id)    # Save results to files
    html_file = save_html_results(game, unique_id)
    print("\n" + format_game_output(game))    # Print the formatted output to terminal
    print(f"\nResults saved to:")
    print(f"- Text file: {os.path.abspath(text_file)}")
    print(f"- HTML file: {os.path.abspath(html_file)}")
    input("\nPress Enter to exit...")    # Add a pause at the end to prevent command window from closing

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        input("\nPress Enter to exit...")
