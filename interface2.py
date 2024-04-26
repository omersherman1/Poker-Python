import pygame
import ast
import socket
import sys
from jsonListener import board_status_data
from collections import deque
import json


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.path = f"img_poker\\{self.suit}{self.rank}.png"
        self.image = pygame.image.load(self.path)

class Player:
    def __init__(self, name, money, bet, hand):
        self.name = name
        self.money = money
        self.bet = bet
        self.hand = [Card(card["Suit"], card["Rank"]) for card in hand]
        self.profile_path = f"img_poker\\{self.name}.png"
        self.profile = pygame.image.load(self.profile_path)
        self.font = pygame.font.Font(None, 36)
        self.money_text = self.font.render(f"Money: {self.money}", True, (0, 0, 0))
        self.bet_text = self.font.render(f"Bet: {self.bet}", True, (0, 0, 0))


class Board:
    def __init__(self, round_number, current_bet, minimum_bet, current_player, community_cards):
        self.round_number = round_number
        self.current_bet = current_bet
        self.minimum_bet = minimum_bet
        self.current_player = current_player
        self.community_cards = [Card(card["Suit"], card["Rank"]) for card in community_cards]

class Game:
    def __init__(self):
        pygame.init()  # Initialize Pygame here
        self.board_status_data = board_status_data
        self.board = self.create_board()
        self.players = self.create_players()
        self.your_name = self.board_status_data["your_name"]
        self.current_player = self.board_status_data["CurrentPlayer"]
        self.current_bet= self.board_status_data["CurrentBet"]

        self.screen_width, self.screen_height = 1920, 1000
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Poker Game")

        self.cloud_background = pygame.image.load(r'clouds.jpg')
        self.cloud_background = pygame.transform.scale(self.cloud_background, (self.screen_width, self.screen_height))
        self.bet_button_clicked = False
        self.bet_amount = 0  # Variable to store the bet amount
        self.bet_text = ""
        self.show_bet_options = True  # Flag to show/hide betting options

        self.card_image_back = pygame.image.load(r'img_poker\back.png')
        self.card_width, self.card_height = self.card_image_back.get_width(), self.card_image_back.get_height()

        self.table_width = 1450
        self.table_height = 650
        self.table_x = (self.screen_width - self.table_width) // 2
        self.table_y = (self.screen_height - self.table_height) // 2
        self.frame_thickness = 10
        self.frame_radius = 150
        self.table_surface = pygame.Surface((self.table_width, self.table_height), pygame.SRCALPHA)
        pygame.draw.rect(self.table_surface, (48, 104, 68), (0, 0, self.table_width, self.table_height), border_radius=self.frame_radius)

    def create_board(self):
        round_number = self.board_status_data["Round"]
        current_bet = self.board_status_data["CurrentBet"]
        minimum_bet = self.board_status_data["MinimumBet"]
        current_player = self.board_status_data["CurrentPlayer"]
        community_cards = self.board_status_data["CommunityCards"]
        return Board(round_number, current_bet, minimum_bet, current_player, community_cards)

    def create_players(self):
        players_data = self.board_status_data["Players"]
        return [Player(player["Name"], player["Money"], player["Bet"], player["Hand"]) for player in players_data]

    def draw(self):
        self.screen.blit(self.cloud_background, (0, 0))
        self.screen.blit(self.table_surface, (self.table_x, self.table_y))
        for i in range(6):
            x = 500 + i * 10
            y = 430
            self.screen.blit(self.card_image_back, (x, y))
        for i, card in enumerate(self.board.community_cards):
            x = 725 + i * 150
            y = 430
            self.screen.blit(card.image, (x, y))

        players_queue = deque()
        for player in self.players:
            players_queue.append(player)

        while players_queue[0].name != self.your_name:
            players_before_you = players_queue.popleft()
            players_queue.append(players_before_you)


        i=0
        while players_queue:
            player = players_queue.popleft()

            if i == 0:  # Bottum
                x = self.table_x + self.table_width // 2 - self.card_width
                y = self.table_y + self.table_height - self.card_height + 20
                self.screen.blit(player.hand[0].image, (x, y))
                self.screen.blit(player.hand[1].image, (x + self.card_width + 15, y))

                profile1_image = pygame.transform.scale(player.profile, (100, 100))
                profile1_surface = pygame.Surface((100, 100))
                profile1_surface.fill((0, 0, 128))
                profile1_surface.blit(profile1_image, (0, 0))
                profile1 = profile1_surface.convert_alpha()
                self.screen.blit(profile1, (x+ self.card_width/2+15, y+150))

                self.screen.blit(player.money_text, (x + self.card_width // 2 + 200, y+90 ))
                self.screen.blit(player.bet_text, (x + self.card_width // 2 + 200, y+40 ))



            elif i== 1:  # Right
                x = self.table_x + self.table_width - self.card_width - 20
                y = self.table_y + self.table_height // 2 - self.card_height // 2
                card1 = pygame.transform.rotate(self.card_image_back, 90)
                card2 = pygame.transform.rotate(self.card_image_back, 90)
                self.screen.blit(card1, (x, y - self.card_width // 2))
                self.screen.blit(card2, (x, y + self.card_width // 2 + 20))

                profile2_image = pygame.transform.scale(player.profile, (100, 100))
                profile2_surface = pygame.Surface((100, 100))
                profile2_surface.fill((	135, 206, 235))  # sky blue background
                profile2_surface.blit(profile2_image, (0, 0))
                profile2 = profile2_surface.convert_alpha()
                self.screen.blit(profile2, (x+150, y))

                self.screen.blit(player.money_text, (x + self.card_width // 2-50 , y+250 ))
                self.screen.blit(player.bet_text, (x + self.card_width // 2-50 , y+200 ))




            elif i == 2:  # Top
                x = self.table_x + self.table_width // 2 - self.card_width
                y = self.table_y - self.card_height + self.card_height - 20
                self.screen.blit(self.card_image_back, (x, y))
                self.screen.blit(self.card_image_back, (x + self.card_width + 15, y))

                profile3_image = pygame.transform.scale(player.profile, (100, 100))
                profile3_surface = pygame.Surface((100, 100))
                profile3_surface.fill((111, 78, 55))
                profile3_surface.blit(profile3_image, (0, 0))
                profile3 = profile3_surface.convert_alpha()
                self.screen.blit(profile3, (x+self.card_width//2 + 7.5, y-120))

                self.screen.blit(player.money_text, (x + self.card_width // 2 - 220, y+100 ))
                self.screen.blit(player.bet_text, (x + self.card_width // 2 - 220, y+50 ))







            else:  # Left
                x = self.table_x - 20
                y = self.table_y + self.table_height // 2 - self.card_height // 2
                card1 = pygame.transform.rotate(self.card_image_back, -90)
                card2 = pygame.transform.rotate(self.card_image_back, -90)
                self.screen.blit(card1, (x, y - self.card_width // 2))
                self.screen.blit(card2, (x, y + self.card_width // 2 + 20))

                profile4_image = pygame.transform.scale(player.profile, (100, 100))
                profile4_surface = pygame.Surface((100, 100))
                profile4_surface.fill((253, 255, 182))
                profile4_surface.blit(profile4_image, (0, 0))
                profile4 = profile4_surface.convert_alpha()
                self.screen.blit(profile4, (x-130,y+10))

                self.screen.blit(player.money_text, (x + self.card_width // 2 , y+250 ))
                self.screen.blit(player.bet_text, (x + self.card_width // 2 , y+200 ))

            i = i+1


        if self.your_name == self.current_player:
            action_button_width = 200
            action_button_height = 50
            action_button_x = 50
            action_button_y = 730
            action_buttons = ["Call", "Bet", "Fold", "Check"]
            for i, button in enumerate(action_buttons):
                pygame.draw.rect(self.screen, (139, 69, 19),
                                 (action_button_x, action_button_y + i * (action_button_height + 10),
                                  action_button_width, action_button_height), border_radius=10)
                font = pygame.font.Font(None, 36)
                text = font.render(button, True, (255, 255, 255))
                text_rect = text.get_rect(
                    center=(action_button_x + action_button_width // 2,
                            action_button_y + i * (action_button_height + 10) + action_button_height // 2))
                self.screen.blit(text, text_rect)
                bet_button_rect = pygame.Rect(action_button_x, action_button_y + 50, action_button_width, action_button_height)

            bet_button_rect = pygame.Rect(action_button_x, action_button_y + 50, action_button_width, action_button_height)
            call_button_rect = pygame.Rect(action_button_x, action_button_y, action_button_width, action_button_height)

            if bet_button_rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked
                    self.bet_button_clicked = True

            if self.bet_button_clicked:
                # Draw betting input field
                bet_input_rect = pygame.Rect(action_button_x + 220, action_button_y + 50, 200, 50)
                pygame.draw.rect(self.screen, (255, 255, 255), bet_input_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), bet_input_rect, 2)

                # Draw typed bet text
                font = pygame.font.Font(None, 36)
                bet_text_surface = font.render(self.bet_text, True, (0, 0, 0))
                self.screen.blit(bet_text_surface, (action_button_x + 225, action_button_y + 55))

                # Handle events for typing bet amount
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            for player in self.players:
                                if player.name == self.current_player:
                                    bet_amount = int(self.bet_text)
                                    player.bet = bet_amount+ player.bet
                                    player.money -= bet_amount
                                    self.bet_button_clicked = False
                                    self.bet_text = ""
                        elif event.key == pygame.K_BACKSPACE:
                            # Handle backspace - remove last character from bet_text
                            self.bet_text = self.bet_text[:-1]
                        # Handle typing of bet amount (numbers)
                        elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                           pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                            typed_number = int(self.bet_text + event.unicode)
                            if typed_number < self.players[0].money:
                                self.bet_text += event.unicode


                # Draw "Confirm", "Cancel", and "All In" buttons
                if self.show_bet_options:  # Only draw if flag is True
                    confirm_button_rect = pygame.Rect(action_button_x + 430, action_button_y + 50, 180, 40)
                    pygame.draw.rect(self.screen, (139, 69, 19), confirm_button_rect)
                    confirm_text = font.render("Confirm", True, (255, 255, 255))
                    self.screen.blit(confirm_text, (action_button_x + 480, action_button_y + 55))

                    cancel_button_rect = pygame.Rect(action_button_x + 430, action_button_y + 110, 180, 40)
                    pygame.draw.rect(self.screen, (139, 69, 19), cancel_button_rect)
                    cancel_text = font.render("Cancel", True, (255, 255, 255))
                    self.screen.blit(cancel_text, (action_button_x + 480, action_button_y + 115))

                    all_in_button_rect = pygame.Rect(action_button_x + 430, action_button_y + 170, 180, 40)
                    pygame.draw.rect(self.screen, (139, 69, 19), all_in_button_rect)
                    all_in_text = font.render("All In", True, (255, 255, 255))
                    self.screen.blit(all_in_text, (action_button_x + 480, action_button_y + 175))

                    # Handle click event on "Cancel" button
                    if cancel_button_rect.collidepoint(pygame.mouse.get_pos()):
                        if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked
                            self.bet_button_clicked = False
                            self.bet_text = ""  # Reset the bet text

                    if confirm_button_rect.collidepoint(pygame.mouse.get_pos()):
                        if pygame.mouse.get_pressed()[0]:
                            for player in self.players:
                                if player.name == self.current_player:
                                    bet_amount = int(self.bet_text)
                                    player.bet = bet_amount+ player.bet
                                    player.money -= bet_amount
                                    self.bet_button_clicked = False
                                    self.bet_text = ""



                    if all_in_button_rect.collidepoint(pygame.mouse.get_pos()):
                        if pygame.mouse.get_pressed()[0]:
                            for player in self.players:
                                if player.name == self.current_player:
                                    player.bet_amount = player.money
                                    player.money = 0
                                    self.bet_button_clicked = False
                                    self.bet_text = ""
                                    player.update_money_text()



        pygame.display.flip()
    def connect_to_server(self):
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        server_address = ("localhost", 8000)  # Replace with your server's address and port
        client_socket.connect(server_address)

        response = client_socket.recv(1024).decode() # getting the board here
        self.board_status_data = ast.literal_eval(response)
        print(self.board_status_data)
        # Send a message to the server
        # message = {}
        # client_socket.send(message.encode())
        # Close the socket
        client_socket.close()
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw()
            clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
json = {
    "Action": "Bet",
    "bet": 2000
}
json = {
    "Action": "Check"
}