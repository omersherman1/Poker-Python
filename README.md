from collections import deque
from player import *
from socketing import Socketing
import threading

class Board:
    def __init__(self, players):
        self.deck = Deck()
        self.community_cards = []
        self.minimum_bet = 50  # Initial minimum bet
        self.current_bet = 0
        self.pot = 0
        self.round_number = 1

        self.players_in_round = []
        self.current_player = Player(players[0])
        self.players = []
        for name in players:
            self.players.append(Player(name))

    def is_round_over(self, last_bettor):
        # Check if it's the last bettor's turn again
        return all(player.bet == 0 or player == last_bettor for player in self.players)

    def play_round(self):
        self.players_in_round = deque([player for player in self.players if player.money > 0])

        print(f"\n--- Round {self.round_number} ---")

        if self.round_number == 1:
            self.deal_initial_hands()
            self.display_board()

        while not len(self.players_in_round) == 0:
            if self.round_number == 2:
                print("\n--- Flop ---")
                self.deal_flop()
                self.display_board()
            elif self.round_number == 3:
                print("\n--- Turn ---")
                self.deal_turn()
                self.display_board()
            elif self.round_number == 4:
                print("\n--- River ---")
                self.deal_river()
                self.display_board()

            self.collect_bets()

        if self.round_number == 4:
            print(self.determine_winner().name)

    def make_bet(self):
        while True:
            try:
                print(f"{self.current_player.name}, your current money: {self.current_player.money}")
                print(f"Previous bet: {self.current_bet}")
                print("1. Fold\n2. Check\n3. Bet\n4. Call\n5. All-In")
                choice = int(input("Enter your choice: "))

                if choice == 1:
                    # Fold
                    self.current_player.bet = 0
                    self.current_player.flag = False
                    return 0
                elif choice == 2:
                    # Check
                    if self.current_bet == 0:
                        self.bet = 0  # Check
                        self.current_player.flag = False
                        return 0
                    else:
                        print("You can't check if a player has bet money. Please choose another option.")
                        continue
                elif choice == 3:
                    # Bet
                    bet_amount = int(input(f"Enter your bet (minimum: {self.minimum_bet}): "))
                    if bet_amount >= self.minimum_bet and bet_amount <= self.current_player.money:
                        self.current_player.bet = bet_amount
                        self.current_player.money -= bet_amount
                        self.current_player.flag = True
                        return bet_amount
                    else:
                        print("Invalid bet amount.")
                elif choice == 4:
                    # Call
                    if self.current_bet == 0:
                        print("There is no bet to call. Please choose another option.")
                        continue
                    elif self.current_player.money >= self.current_bet:
                        self.current_player.bet = self.current_bet  # Call
                        self.current_player.money -= self.current_bet
                        self.current_player.flag = False
                        return self.current_bet
                    else:
                        print("Not enough money to call. Please choose another option.")
                        continue
                elif choice == 5:
                    # All-In
                    self.current_player.bet = self.current_player.money
                    self.current_player.money = 0
                    self.current_player.flag = True
                    return self.current_player.bet
                else:
                    print("Invalid choice. Please enter a valid option.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def collect_bets(self):
        players_checked = []

        self.minimum_bet = 50

        while len(self.players_in_round) > 0:  # Continue until only one player remains in the round
            self.current_player = self.players_in_round[0]

            if self.current_player.money > 0:
                self.minimum_bet = max(self.current_bet, self.minimum_bet)
                bet_made = self.make_bet()

                if bet_made != self.current_bet: # bet or raise (and of course, all in) were made
                    self.minimum_bet = bet_made + 50

                    self.current_player.bet = bet_made
                    self.current_bet = bet_made
                    self.players_in_round.extend(players_checked)
                    players_checked = []
                    players_checked.append(self.current_player)
                else: # check or call
                    players_checked.append(self.current_player)

            self.players_in_round.popleft()


    def deal_flop(self):
        for card in range(3):
            self.community_cards.append(self.deck.draw_card())

    def deal_turn(self):
        self.community_cards.append(self.deck.draw_card())

    def deal_river(self): # River should open ALL cards on board. Now it opens only 1. What if all players go All-In?
        self.community_cards.append(self.deck.draw_card())

    def display_board(self):
        print("Community Cards:")
        for card in self.community_cards:
            print(str(card))
        if len(self.community_cards) == 0:
            print("No Community Cards Open")

        print("--- Players Hands ---")
        for player in self.players:
            print(f"{player.name}'s hand: {', '.join(str(card) for card in player.hand)}")

    def determine_winner(self):
        # In a real poker game, you would implement hand evaluation logic
        winning_player = max(self.players, key=lambda player: player.hand[0].rank)
        winning_player.money += self.pot
        self.pot = 0
        return winning_player

    def deal_initial_hands(self):
        for player in self.players:
            player.draw_hand(self.deck)

def makequeue(players):
    queue = deque(players)
    return queue

if __name__ == "__main__":

    socketing = Socketing()
    # Start the server in a separate thread
    server_thread = threading.Thread(target=socketing.start_server)
    server_thread.start()
    player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]

    poker_game = Board(player_names)

    queue = makequeue(poker_game.players)

    while True:
        poker_game.play_round()
        # playerturn(queue)

        # Check if any player is out of money
        if any(player.money <= 0 for player in poker_game.players):
            print("Game over!")
            break
        poker_game.round_number += 1  # Increment round number
