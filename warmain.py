import sys
import random
import datetime
import os

class Card:
    # assigning the card nd its values
    SUITS = ['♥', '♦', '♣', '♠']  # four card types
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', 'Joker']  # Card values

    def __init__(self, rank, suit=None):
        # initilizing a card with a value nd a type
        self.rank = rank
        self.suit = suit

    def __str__(self):
        #assining sting to a card if its not the joker
        if self.rank == 'Joker':
            return f"Joker{self.suit if self.suit else '♥'}"
        return f"{self.rank}{self.suit}"

    def get_value(self):
        # getting a numeric value of a card based on value
        return Card.RANKS.index(self.rank)

class Deck:
    #a full deck of card and giving the process of how to shuffle.
    def __init__(self):
        self.cards = []  # initializing a list to keep the card as a deck
        self._initialize_deck() 

    def _initialize_deck(self):
        # adding the cards to a desck with 52 cards nd 2 joker cards
        for suit in Card.SUITS:
            for rank in Card.RANKS[:-1]:  # excluding the joker card
                self.cards.append(Card(rank, suit))
        
        # adding joker cards  
        self.cards.append(Card('Joker', '♥'))
        self.cards.append(Card('Joker', '♠'))

    def shuffle(self):
        # randomizing the deck
        random.shuffle(self.cards)

    def deal(self, num_players=2):
        # distrubing the cards to players evenly
        if num_players <= 0:
            return []
        
        hands = [[] for _ in range(num_players)]
        for i, card in enumerate(self.cards):
            hands[i % num_players].append(card)
        
        return hands

class GameHistory:
    #keeping the hoistory of the game nd saving them
    def __init__(self):
        self.history = []  
        self.start_time = datetime.datetime.now()  
        self.end_time = None  
        self.total_rounds = 0 
        self.human_cards = 0 
        self.pc_cards = 0 
        self.winner = None  
        self.war_count = 0

    def add_round_result(self, round_num, play_num, human_card, pc_card, winner, is_war=False, war_cards=None):
        #recording the results of each round
        result = {
            'round': round_num,
            'play_num': play_num,
            'human_card': str(human_card),
            'pc_card': str(pc_card),
            'winner': winner,
            'is_war': is_war
        }
        
        if is_war and war_cards:
            # If war happens saving it details
            result['war_cards'] = war_cards
            self.war_count += 1
            
        self.history.append(result) 

    def set_game_result(self, human_cards, pc_cards, winner):
        """Record the final results of the game."""
        self.end_time = datetime.datetime.now()  # Recording the end time
        self.human_cards = human_cards
        self.pc_cards = pc_cards
        self.winner = winner  # winner of the game

    def save_to_file(self):
        #saving the history of the game in a file
        now = datetime.datetime.now()
        random_num = random.randint(1000, 9999)
        filename = f"{now.strftime('%Y%m%d')[2:]}_{now.strftime('%H-%M')}_{random_num}"
        
        # Save the history in text and HTML files
        self._save_as_text(filename + ".txt")
        self._save_as_html(filename + ".html")
        
        return filename

    def _save_as_text(self, filename):
        with open(filename, 'w') as file:
            # adding the headings 
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.datetime.now().strftime('%H:%M')
            
            file.write(f"Date : {current_date}\n")
            file.write(f"Time : {current_time}\n\n")
            file.write(f"Total Rounds : {self.total_rounds}\n\n")
            
            #organize part
            round_plays = {}
            for play in self.history:
                round_num = play['round']
                if round_num not in round_plays:
                    round_plays[round_num] = []
                round_plays[round_num].append(play)
            
            # writing the results to file
            for round_num in sorted(round_plays.keys()):
                file.write(f"Round {round_num} results\n")
                file.write("-------------------------\n")
                file.write("No : Hum vs PC - Winner\n")
                
                for play in round_plays[round_num]:
                    play_num = play['play_num']
                    human_card = play['human_card']
                    pc_card = play['pc_card']
                    
                    if play['is_war']:
                        winner_text = "WAR"
                    else:
                        winner_text = "HUMAN" if play['winner'] == "Human" else "PC"
                    
                    file.write(f"{play_num} : {human_card} vs {pc_card} - {winner_text}\n")
                
                file.write("\n")
            
            # Writing the final results
            file.write(f"PC card count {self.pc_cards}\n")
            file.write(f"Human card count {self.human_cards}\n")
            file.write(f"War count {self.war_count}\n\n")
            
            if self.winner == "Tie":
                file.write("The game ended in a tie!\n")
            else:
                file.write(f"{self.winner} won the game!\n")

    def _save_as_html(self, filename):
        #saving the hsitory in html file
        with open(filename, 'w') as file:
            file.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>War Card Game Results</title>
    <style>
        body { 
            font-family: monospace; 
            white-space: pre;
            margin: 20px;
        }
    </style>
</head>
<body>
""")
        

            current_date = datetime.datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.datetime.now().strftime('%H:%M')
        
            file.write(f"Date : {current_date}\n")
            file.write(f"Time : {current_time}\n\n")
            file.write(f"Total Rounds : {self.total_rounds}\n\n")
        
           
            round_plays = {}
            for play in self.history:
                round_num = play['round']
                if round_num not in round_plays:
                    round_plays[round_num] = []
                round_plays[round_num].append(play)
        
           
            for round_num in sorted(round_plays.keys()):
                file.write(f"Round {round_num} results\n")
                file.write("-----------------------------\n")
                file.write("No : Hum vs PC - Winner\n")
            
                for play in round_plays[round_num]:
                    play_num = play['play_num']
                    human_card = play['human_card']
                    pc_card = play['pc_card']
                
                    if play['is_war']:
                        winner_text = "WAR"
                    else:
                        winner_text = "HUMAN" if play['winner'] == "Human" else "PC"
                
                    file.write(f"{play_num} : {human_card} vs {pc_card} - {winner_text}\n")
            
                file.write("\n")
        
            file.write(f"PC card count {self.pc_cards}\n")
            file.write(f"Human card count {self.human_cards}\n")
            file.write(f"War count {self.war_count}\n\n")
        
            if self.winner == "Tie":
                file.write("The game ended in a tie!\n")
            else:
                file.write(f"{self.winner} won the game!\n")
        
            file.write("""</body>
</html>""")

class WarGame:
    def __init__(self, rounds=1):
        self.rounds = max(1, min(5, rounds))  # Limit rounds to 1-5
        self.human_cards = []
        self.pc_cards = []
        self.human_pile = []
        self.pc_pile = []
        self.game_history = GameHistory()
    
    def setup_game(self):
        #setting the deal cards
        print("=== WAR CARD GAME ===")
        print(f"Playing {self.rounds} round(s)")
        
        # Create and shuffling the card deck
        deck = Deck()
        deck.shuffle()
        
        hands = deck.deal(2)
        self.human_cards = hands[0]
        self.pc_cards = hands[1]
        
        random.shuffle(self.human_cards)
        random.shuffle(self.pc_cards)
        
        print(f"Cards dealt: Human has {len(self.human_cards)} cards, PC has {len(self.pc_cards)} cards")
        print("Game starts...\n")
    
    def play_round(self, round_num):
        #single round
        print(f"=== Round {round_num} ===")
        
        play_count = 0
        while play_count < 27:
            # Checking if any player has run out of cards
            if not self.human_cards or not self.pc_cards:
                break
            
            play_count += 1
            
            # Drawing cards
            human_card = self.human_cards.pop(0)
            pc_card = self.pc_cards.pop(0)
            
            print(f"Play {play_count}: Human plays {human_card} - PC plays {pc_card}")
            
            # Comparing cards
            if human_card.get_value() > pc_card.get_value():
                winner = "Human"
                self.human_pile.extend([human_card, pc_card])
                print(f"{winner} wins this play")
                self.game_history.add_round_result(round_num, play_count, human_card, pc_card, winner)
            elif pc_card.get_value() > human_card.get_value():
                winner = "PC"
                self.pc_pile.extend([human_card, pc_card])
                print(f"{winner} wins this play")
                self.game_history.add_round_result(round_num, play_count, human_card, pc_card, winner)
            else:
                # War! Both cards are equal
                print("WAR! Both cards are equal")
                winner, war_cards = self._handle_war(human_card, pc_card)
                self.game_history.add_round_result(round_num, play_count, human_card, pc_card, winner, True, war_cards)
            
            print("")
            
            # checing again if any player runed out of cards
            if not self.human_cards or not self.pc_cards:
                break
    
    def _handle_war(self, human_card, pc_card):
        """Handle a war situation when both players draw equal cards"""
        print("Drawing 3 hidden cards and 1 visible card...")
        
        if len(self.human_cards) < 4 or len(self.pc_cards) < 4:
            human_war_cards = self.human_cards[:3]
            pc_war_cards = self.pc_cards[:3]
            self.human_cards = self.human_cards[3:]
            self.pc_cards = self.pc_cards[3:]
            
            if not self.human_cards:
                print("Human doesn't have enough cards for war. PC wins!")
                self.pc_pile.extend([human_card, pc_card] + human_war_cards + pc_war_cards)
                return "PC", {"human": "No cards", "pc": "No cards"}
            
            if not self.pc_cards:
                print("PC doesn't have enough cards for war. Human wins!")
                self.human_pile.extend([human_card, pc_card] + human_war_cards + pc_war_cards)
                return "Human", {"human": "No cards", "pc": "No cards"}
        
        # Drawing three faces down as in the video
        human_war_cards = [self.human_cards.pop(0) for _ in range(3)]
        pc_war_cards = [self.pc_cards.pop(0) for _ in range(3)]
        
        # Drawing the fourth card up face showing the value
        human_war_card = self.human_cards.pop(0) if self.human_cards else None
        pc_war_card = self.pc_cards.pop(0) if self.pc_cards else None
        
        # If any player runs out of cards
        if not human_war_card:
            print("Human doesn't have enough cards for war. PC wins!")
            self.pc_pile.extend([human_card, pc_card] + human_war_cards + pc_war_cards)
            return "PC", {"human": "No cards", "pc": str(pc_war_card) if pc_war_card else "No cards"}
        
        if not pc_war_card:
            print("PC doesn't have enough cards for war. Human wins!")
            self.human_pile.extend([human_card, pc_card] + human_war_cards + pc_war_cards)
            return "Human", {"human": str(human_war_card), "pc": "No cards"}
        
        # Comparing the fourth card
        print(f"War cards revealed: Human plays {human_war_card} - PC plays {pc_war_card}")
        
        all_cards = [human_card, pc_card] + human_war_cards + pc_war_cards + [human_war_card, pc_war_card]
        
        if human_war_card.get_value() > pc_war_card.get_value():
            winner = "Human"
            self.human_pile.extend(all_cards)
            print(f"{winner} wins this war!")
        elif pc_war_card.get_value() > human_war_card.get_value():
            winner = "PC"
            self.pc_pile.extend(all_cards)
            print(f"{winner} wins this war!")
        else:
            print("Another war! Cards are still equal")
            winner, nested_war_cards = self._handle_war(human_war_card, pc_war_card)
            
            if winner == "Human":
                self.human_pile.extend(all_cards)
            else:
                self.pc_pile.extend(all_cards)
            
            return winner, nested_war_cards
        
        return winner, {"human": str(human_war_card), "pc": str(pc_war_card)}
    
    def determine_winner(self):
        #checking the cards and deciding the winner
        human_total = len(self.human_pile)
        pc_total = len(self.pc_pile)
        
        print("\n=== FINAL RESULT ===")
        print(f"Human cards: {human_total}")
        print(f"PC cards: {pc_total}")
        print(f"War count: {self.game_history.war_count}")
        
        if human_total > pc_total:
            winner = "Human"
        elif pc_total > human_total:
            winner = "PC"
        else:
            winner = "Tie"
        
        print(f"Winner: {winner}!\n")
        
        return human_total, pc_total, winner
    
    def play_game(self):
        self.setup_game()
        
        for round_num in range(1, self.rounds + 1):
            self.play_round(round_num)
            
            #reseting the card to players again
            self.human_cards.extend(self.human_pile)
            self.pc_cards.extend(self.pc_pile)
            self.human_pile = []
            self.pc_pile = []
            
            # Shuffling
            random.shuffle(self.human_cards)
            random.shuffle(self.pc_cards)
            
            print(f"End of round {round_num}. Reshuffling cards...\n")
        
        self.game_history.total_rounds = self.rounds
        
        human_total, pc_total, winner = self.determine_winner()
        
        self.game_history.set_game_result(human_total, pc_total, winner)
        
        filename = self.game_history.save_to_file()
        print(f"Game history saved to {filename}.txt and {filename}.html")
        
        return winner

def view_history():
    #viewing the history
    print("=== VIEW PAST GAME HISTORY ===")
    
    text_files = [f for f in os.listdir('.') if f.endswith('.txt') and len(f) > 4]
    
    if not text_files:
        print("No past game history found.")
        return
    
    # Sorting file according to the time
    text_files.sort(key=lambda x: os.path.getctime(x), reverse=True)
    
    print(f"Found {len(text_files)} past game records:")
    for i, file in enumerate(text_files):
        print(f"{i+1}. {file}")
    
    # asking which file to view
    try:
        choice = int(input("\nEnter number to view (0 to cancel): "))
        if 1 <= choice <= len(text_files):
            file_to_view = text_files[choice-1]
            print(f"\nViewing {file_to_view}:\n")
            
            with open(file_to_view, 'r') as file:
                print(file.read())
    except (ValueError, IndexError):
        print("Invalid selection.")

def main():
    #to handle the cli input
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "history":
            view_history()
            return
        
        try:
            rounds = int(sys.argv[1])
            if not 1 <= rounds <= 5:
                print("Number of rounds must be between 1 and 5.")
                rounds = 1
        except ValueError:
            print("Invalid argument. Using default 1 round.")
            rounds = 1
    else:
        rounds = 1
    
    # Create and play the game
    game = WarGame(rounds)
    game.play_game()

if __name__ == "__main__":
    main()