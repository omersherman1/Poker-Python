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

        self.players_in_round = []
        self.current_player = Player(players[0])
        self.players = []
        for name in players:
            self.players.append(Player(name))

    def play_round(self, client_socket):
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

            self.collect_bets(client_socket)

        if self.round_number == 4:
            print(self.determine_winner().name)

    def make_bet(self, jsonFromClient):
        choice = jsonFromClient["action"]
        bet_amount = jsonFromClient.get("bet", 0)

        if choice == "fold":
            # Fold
            self.current_player.bet = 0
            self.current_player.flag = False
            return 0
        elif choice == "check":
            # Check
            if self.current_bet == 0:
                self.current_player.bet = 0  # Check
                self.current_player.flag = False
                return 0
            else:
                print("You can't check if a player has bet money. Please choose another option.")
                return self.make_bet(jsonFromClient)  # ask again
        elif choice == "bet":
            # Bet
            if bet_amount >= self.minimum_bet and bet_amount <= self.current_player.money:
                self.current_player.bet = bet_amount
                self.current_player.money -= bet_amount
                self.current_player.flag = True
                return bet_amount
            else:
                print("Invalid bet amount.")
                return self.make_bet(jsonFromClient)  # ask again
        elif choice == "call":
            # Call
            if self.current_bet == 0:
                print("There is no bet to call. Please choose another option.")
                return self.make_bet(jsonFromClient)  # ask again
            elif self.current_player.money >= self.current_bet:
                self.current_player.bet = self.current_bet  # Call
                self.current_player.money -= self.current_bet
                self.current_player.flag = False
                return self.current_bet
            else:
                print("Not enough money to call. Please choose another option.")
                return self.make_bet(jsonFromClient)  # ask again
        elif choice == "all in":
            # All-In
            self.current_player.bet = self.current_player.money
            self.current_player.money = 0
            self.current_player.flag = True
            return self.current_player.bet
        else:
            print("Invalid choice. Please enter a valid option.")
            return self.make_bet(jsonFromClient)  # ask again

    def collect_bets(self, client_socket):
        players_checked = []

        self.minimum_bet = 50

        while len(self.players_in_round) > 0:  # Continue until only one player remains in the round
            self.current_player = self.players_in_round[0]

            if self.current_player.money > 0:
                self.minimum_bet = max(self.current_bet, self.minimum_bet)

                self.send_board_to_client(client_socket)
                print("Waiting for " + self.current_player.name + " input")
                message = client_socket.recv(1024).decode()
                json_from_client = json.loads(message)
                print(json_from_client['action'])

                bet_made = self.make_bet(json_from_client)

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

    def send_board_to_client(self, client_socket):
        data_for_client = {
            'Community Cards': [],
            'Players': []
        }

        data_for_client["Current Player"] = self.current_player.name
        data_for_client["Round"] = self.round_number
        data_for_client["Current Bet"] = self.current_bet
        data_for_client["Minimum Bet"] = self.minimum_bet

        for card in self.community_cards:
            data_for_client['Community Cards'].append(card.__dict__())

        for player in self.players:
            data_for_client['Players'].append(player.__dict__())

        client_socket.sendall(json.dumps(data_for_client).encode())


class PokerGameServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = {}
        self.board = Board(["Player1", "Player2", "Player3", "Player4"])

    def handle_client(self, client_socket, client_address):
        print(f"Connected by {client_address}")

        try:
            while True:
                self.board.play_round(client_socket)

                # Check if any player is out of money
                if any(player.money <= 0 for player in self.board.players):
                    print("Game over!")
                    break
                self.board.round_number += 1  # Increment round number

        except ConnectionResetError:
            print(f"Disconnected by {client_address}")
        except Exception as e:
            print(f"Error handling client {client_address}: {str(e)}")
        finally:
            del self.clients[client_address]
            client_socket.close()

    def start(self):
        print("Poker game server started")
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.clients[client_address] = client_socket
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    server = PokerGameServer("localhost", 8000)
    server.start()

