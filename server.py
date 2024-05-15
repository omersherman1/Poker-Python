import json
import socket
import threading
from collections import deque

from player import *


class Board:
    def __init__(self, players):
        self.deck = Deck()
        self.community_cards = []
        self.minimum_bet = 50  # Initial minimum bet
        self.current_bet = 0
        self.pot = 0
        self.round_number = 1
        self.status = None

        self.players_in_round = []
        self.current_player = Player(players[0])
        self.players = []
        for name in players:
            self.players.append(Player(name))

    def play_round(self, clients):
        self.players_in_round = deque([player for player in self.players if player.money > 0 and player.is_fold!= True])
        print(f"\n--- Round {self.round_number} ---")

        if self.round_number == 1:
            self.deal_initial_hands()
        self.evaluate_all_hands()
        while not len(self.players_in_round) == 0:
            if self.round_number == 2:
                print("\n--- Flop ---")
                self.deal_flop()
                self.evaluate_all_hands()
            elif self.round_number == 3:
                print("\n--- Turn ---")
                self.deal_turn()
                self.evaluate_all_hands()

            elif self.round_number == 4:
                print("\n--- River ---")
                self.deal_river()
                self.evaluate_all_hands()

            self.display_board()
            self.collect_bets(clients)

        if self.round_number == 4:
            winning_player = self.determine_winner()
            winning_player.money += self.pot
            self.pot = 0
            self.reset_board()  # Reset the board after determining the winner

    def evaluate_all_hands(self):
        for player in self.players:
            player.combination(player.hand[0], player.hand[1], self.community_cards)

    def reset_board(self):
        self.deck = Deck()
        self.community_cards = []
        self.minimum_bet = 50
        self.round_number = 0
        self.status = None
        for player in self.players:
            player.hand = []
            player.current_best_combination = "None"
            player.current_score = 0

        self.deal_initial_hands()  # Deal new hands to all players

    def deal_initial_hands(self):
        for player in self.players:
            player.draw_hand(self.deck)

    def make_bet(self, jsonFromClient, clients):
        choice = jsonFromClient["action"]
        bet_amount = jsonFromClient.get("bet", 0)

        if choice == "fold":
            # Fold
            self.current_player.is_fold = True
            self.current_player.bet = 0
            return 0

        elif choice == "check":
            # Check
            if self.current_bet == 0:
                self.current_player.bet = 0  # Check
                return 0

            else:
                self.status = "You can't check if a player has bet money. Please choose another option."

                self.send_board_to_all_clients(clients)
                print("Waiting for " + self.current_player.name + " input")
                json_from_client = json.loads(clients.get(self.current_player.name).recv(1024).decode())

                return self.make_bet(json_from_client, clients)  # ask again

        elif choice == "bet":
            if bet_amount >= self.minimum_bet and bet_amount <= self.current_player.money:
                self.current_player.bet = bet_amount
                self.current_player.money -= bet_amount
                self.pot = self.pot + bet_amount
                return bet_amount

            else:
                self.status = "Invalid bet amount."
                print("Invalid bet amount.")

                self.send_board_to_all_clients(clients)
                print("Waiting for " + self.current_player.name + " input")
                json_from_client = json.loads(clients.get(self.current_player.name).recv(1024).decode())
                return self.make_bet(json_from_client, clients)  # ask again

        elif choice == "call":
            # Call
            if self.current_bet == 0:
                self.status = "There is no bet to call. Please choose another option."
                print("There is no bet to call. Please choose another option.")

                self.send_board_to_all_clients(clients)
                print("Waiting for " + self.current_player.name + " input")
                json_from_client = json.loads(clients.get(self.current_player.name).recv(1024).decode())
                return self.make_bet(json_from_client, clients)  # ask again

            elif self.current_player.money >= self.current_bet:
                self.current_player.bet = self.current_bet  # Call
                self.current_player.money -= self.current_bet
                self.pot = self.pot + self.current_player.bet
                return self.current_bet

            else:
                self.status = "Not enough money to call. Please choose another option."
                print("Not enough money to call. Please choose another option.")

                self.send_board_to_all_clients(clients)
                print("Waiting for " + self.current_player.name + " input")
                json_from_client = json.loads(clients.get(self.current_player.name).recv(1024).decode())

                return self.make_bet(json_from_client, clients)  # ask again

        elif choice == "all in":
            # All-In
            self.current_player.bet = self.current_player.money
            self.current_player.money = 0
            self.pot = self.pot + self.current_player.money
            return self.current_player.bet

        else:
            print("Invalid choice. Please enter a valid option.")

            self.send_board_to_all_clients(clients)
            print("Waiting for " + self.current_player.name + " input")
            json_from_client = json.loads(clients.get(self.current_player.name).recv(1024).decode())
            return self.make_bet(json_from_client, clients)  # ask again

    def collect_bets(self, clients):
        players_checked = []
        self.minimum_bet = 50

        while len(self.players_in_round) > 0:  # Continue until only one player remains in the round
            self.current_player = self.players_in_round[0]

            if self.current_player.money > 0:
                self.minimum_bet = max(self.current_bet, self.minimum_bet)

                self.send_board_to_all_clients(clients)

                print("Waiting for " + self.current_player.name + " input")
                message = clients.get(self.current_player.name).recv(1024).decode()
                print(message)
                json_from_client = json.loads(message)
                bet_made = self.make_bet(json_from_client, clients)

                if bet_made != self.current_bet:  # bet or raise (and of course, all in) were made
                    self.minimum_bet = bet_made + 50

                    self.current_player.bet = bet_made
                    self.current_bet = bet_made
                    self.players_in_round.extend(players_checked)
                    players_checked = [self.current_player]
                else:  # check or call
                    players_checked.append(self.current_player)

            self.players_in_round.popleft()
            self.status = None

    def deal_flop(self):
        for card in range(3):
            self.community_cards.append(self.deck.draw_card())

    def deal_turn(self):
        self.community_cards.append(self.deck.draw_card())

    def deal_river(self):  # River should open ALL cards on board. Now it opens only 1. What if all players go All-In?
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
        active_players = [player for player in self.players if not player.fold]
        winning_player = max(self.players, key=lambda player: player.current_score)
        winning_player.money += self.pot
        self.pot = 0
        return winning_player

    def deal_initial_hands(self):
        for player in self.players:
            player.draw_hand(self.deck)

    def send_board_to_all_clients(self, clients):
        data_for_client = {'Community Cards': [],
                           'Players': [],
                           "Current Player": self.current_player.name,
                           "Round": self.round_number,
                           "Minimum Bet": self.minimum_bet,
                           "Status": self.status,
                           "Pot": self.pot}

        for card in self.community_cards:
            data_for_client['Community Cards'].append(card.__dict__())

        for player in self.players:
            data_for_client['Players'].append(player.__dict__())

        for client_socket in clients.values():
            client_socket.sendall(json.dumps(data_for_client).encode())


class PokerGameServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = {}
        self.board = None

    def handle_client(self, client_socket, client_address, position):
        print(f"Connected by {client_address}")

    def accept_clients(self):
        while len(self.clients) < 4:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address} established.")
            player_name = json.loads(client_socket.recv(1024).decode())["Player Name"]
            print(player_name)
            self.clients[player_name] = client_socket

    def get_clients(self):
        return self.clients

    def start(self):
        print("Poker game server started")

        threading.Thread(target=self.accept_clients).start()

        while True:
            if len(self.clients) == 4:
                players = [player_name for player_name in self.clients.keys()]
                self.board = Board(players)

                while True:
                    self.board.play_round(self.clients)

                    # Check if any player is out of money
                    if any(player.money <= 0 for player in self.board.players):
                        print("Game over!")
                        break

                    for player in self.board.players:
                        player.bet = 0
                    self.board.current_bet = 0
                    self.board.round_number += 1  # Increment round number

                self.clients.clear()

if __name__ == "__main__":
    server = PokerGameServer("localhost", 8000)
    server.start()