import ast
import asyncio
import socket
from threading import Thread
from time import sleep

import pygame
import sys
# from Server.jsonListener import board_status_data
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
        self.hand = [Card(card["suit"], card["rank"]) for card in hand]
        self.profile_path = f"img_poker\\{self.name}.png"
        self.profile = pygame.image.load(self.profile_path)
        self.font = pygame.font.Font(None, 36)
        self.name_text = self.font.render(f"{self.name}", True, (255,255,255))
        self.money_text = self.font.render(f"Money: {self.money}", True, (0, 0, 0))
        self.bet_text = self.font.render(f"Bet: {self.bet}", True, (0, 0, 0))


class Board:
    def __init__(self, round_number, current_bet, minimum_bet, current_player, community_cards):
        self.round_number = round_number
        self.current_bet = current_bet
        self.minimum_bet = minimum_bet
        self.current_player = current_player
        self.community_cards = [Card(card["suit"], card["rank"]) for card in community_cards]
        self.font = pygame.font.Font(None, 36)
        self.round_text = self.font.render(f"Round: {self.round_number}", True, (0, 0, 0))


class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.clicked = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + self.rect.width // 3, self.rect.y + self.rect.height // 3.5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False

    def is_clicked(self):
        return self.clicked


class Table:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.table_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

    def draw(self, screen):
        pygame.draw.rect(self.table_surface, self.color, (0, 0, self.rect.width, self.rect.height), border_radius=150)
        screen.blit(self.table_surface, (self.rect.x, self.rect.y))


class PlayerProfile:
    def __init__(self, player, x, y, back_card, color, current_player, index):
        self.Player = player
        self.x = x
        self.y = y
        self.back_card = back_card
        self.color = color
        self.current_player = current_player
        self.index = index

    def profile_maker(self):
        profile_image = pygame.transform.scale(self.Player.profile, (100, 100))
        profile_surface = pygame.Surface((100, 100))
        profile_surface.fill(self.color)
        profile_surface.blit(profile_image, (0, 0))
        return profile_surface.convert_alpha()

    def draw(self, screen):
        card1 = pygame.transform.rotate(self.back_card, self.index * 90)
        card2 = pygame.transform.rotate(self.back_card, self.index * 90)
        screen.blit(self.profile_maker(), (self.x, self.y))
        if self.index == 0:
            card1 = pygame.transform.rotate(self.Player.hand[0].image, self.index * 90)
            card2 = pygame.transform.rotate(self.Player.hand[1].image, self.index * 90)
            screen.blit(card1, (self.x + 60, self.y - 150))
            screen.blit(card2, (self.x - 60, self.y - 150))
            screen.blit(self.Player.name_text, (self.x + 170, self.y - 150))
            screen.blit(self.Player.money_text, (self.x + 170, self.y - 120))
            screen.blit(self.Player.bet_text, (self.x + 170, self.y - 90))
            if self.Player.name == self.current_player:
                pygame.draw.circle(screen, (255,255,255), (self.x+150, self.y+50), 25)
        elif self.index == 1:
            screen.blit(card1, (self.x - 150, self.y + 60))
            screen.blit(card2, (self.x - 150, self.y - 60))
            screen.blit(self.Player.name_text, (self.x - 220, self.y - 165))
            screen.blit(self.Player.money_text, (self.x - 220, self.y - 135))
            screen.blit(self.Player.bet_text, (self.x - 220, self.y - 105))
            if self.Player.name == self.current_player:
               pygame.draw.circle(screen, (139, 0, 0), (self.x + 50, self.y - 50), 25)
        elif self.index == 2:
            screen.blit(card1, (self.x + 60, self.y + 120))
            screen.blit(card2, (self.x - 60, self.y + 120))
            screen.blit(self.Player.name_text, (self.x -250, self.y + 150))
            screen.blit(self.Player.money_text, (self.x - 250, self.y + 180))
            screen.blit(self.Player.bet_text, (self.x - 250, self.y + 210))
            if self.Player.name == self.current_player:
               pygame.draw.circle(screen, (255,255,255), (self.x - 50, self.y + 50 ), 25)
        elif self.index == 3:
            screen.blit(card1, (self.x + 170, self.y + 60))
            screen.blit(card2, (self.x + 170, self.y - 60))
            screen.blit(self.Player.name_text, (self.x + 170, self.y - 165))
            screen.blit(self.Player.money_text, (self.x + 170, self.y - 135))
            screen.blit(self.Player.bet_text, (self.x + 170, self.y - 105))
            if self.Player.name == self.current_player:
               pygame.draw.circle(screen, (255,255,255), (self.x + 50, self.y+ 150), 25)


class Game:
    def __init__(self):
        pygame.init()  # Initialize Pygame here
        self.board_status_data = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()
        self.board = None
        self.players = None
        self.current_player = None

        self.bottom_player = None
        self.right_player = None
        self.top_player = None
        self.left_player = None

        action_button_x = 50
        action_button_y = 750
        action_button_width = 200
        action_button_height = 50
        action_button_color = (139, 69, 19)
        self.check_button = Button(action_button_x, action_button_y + 0 * (action_button_height + 10),
                                   action_button_width, action_button_height, "Check", action_button_color)
        self.bet_button = Button(action_button_x, action_button_y + 1 * (action_button_height + 10),
                                 action_button_width, action_button_height, "Bet", action_button_color)
        self.call_button = Button(action_button_x, action_button_y + 2 * (action_button_height + 10),
                                  action_button_width, action_button_height, "Call", action_button_color)
        self.fold_button = Button(action_button_x, action_button_y + 3 * (action_button_height + 10),
                                  action_button_width, action_button_height, "Fold", action_button_color)
        self.confirm_button = Button(action_button_x + 430, action_button_y + 1 * (action_button_height + 10),
                                     action_button_width, action_button_height, "Confirm", action_button_color)
        self.cancel_button = Button(action_button_x + 430, action_button_y + 2 * (action_button_height + 10),
                                    action_button_width, action_button_height, "Cancel", action_button_color)
        self.all_in_button = Button(action_button_x + 430, action_button_y + 3 * (action_button_height + 10),
                                    action_button_width, action_button_height, "All In", action_button_color)
        self.action_buttons = [self.check_button, self.bet_button, self.call_button, self.fold_button,
                               self.confirm_button, self.cancel_button, self.all_in_button]

        self.screen_width = 1920
        self.screen_height = 1000
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Poker Game")

        self.cloud_background = pygame.transform.scale(pygame.image.load(r'clouds.jpg'),
                                                       (self.screen_width, self.screen_height))
        self.last_bet_amount = 0
        self.bet_amount = 0
        self.bet_text = ""
        self.show_bet_options = False

        self.card_image_back = pygame.image.load(r'img_poker\back.png')
        self.card_width = self.card_image_back.get_width()
        self.card_height = self.card_image_back.get_height()

        self.table = Table((self.screen_width - 1450) // 2, (self.screen_height - 650) // 2, 1450, 650, (48, 104, 68))

    def connect_to_server(self):
        self.socket.connect(("localhost", 8000))

    def send_action_to_server(self, action):
        json_data = {"action": action}
        if action == 'bet':
            json_data['bet'] = int(self.bet_text)
        print(json_data)
        self.socket.sendall(json.dumps(json_data).encode())

    def update_game_state(self):
        response = self.socket.recv(1024).decode()
        if response:
            self.board_status_data = json.loads(response)
            self.board = self.create_board()
            self.players = self.create_players()
            self.current_player = self.board_status_data["Current Player"]

    def create_board(self):
        round_number = self.board_status_data["Round"]
        current_bet = self.board_status_data["Current Bet"]
        minimum_bet = self.board_status_data["Minimum Bet"]
        current_player = self.board_status_data["Current Player"]
        community_cards = self.board_status_data["Community Cards"]
        return Board(round_number, current_bet, minimum_bet, current_player, community_cards)

    def create_players(self):
        players_data = self.board_status_data["Players"]
        return [Player(player["name"], player["money"], player["bet"], player["hand"]) for player in players_data]

    def draw(self):
        try:
            self.screen.blit(self.cloud_background, (0, 0))
            self.table.draw(self.screen)
            for i in range(6):
                x = 500 + i * 10
                y = 430
                self.screen.blit(self.card_image_back, (x, y))
            last_index = -1
            for i, card in enumerate(self.board.community_cards):
                x = 725 + i * 150
                y = 430
                last_index = i
                self.screen.blit(card.image, (x, y))
            while last_index < 4:
                last_index += 1
                x = 725 + last_index * 150
                y = 430
                self.screen.blit(self.card_image_back, (x, y))

            players_queue = deque()
            for player in self.players:
                players_queue.append(player)

            while players_queue[0].name != self.current_player:
                players_queue.append(players_queue.popleft())

            self.bottom_player = PlayerProfile(players_queue[0], 920, 850, self.card_image_back, (0, 0, 128),
                                               self.current_player, 0)
            self.right_player = PlayerProfile(players_queue[1], 1730, 450, self.card_image_back, (135, 206, 235),
                                              self.current_player, 1)
            self.top_player = PlayerProfile(players_queue[2], 920, 50, self.card_image_back, (111, 78, 55),
                                            self.current_player, 2)
            self.left_player = PlayerProfile(players_queue[3], 85, 450, self.card_image_back, (253, 255, 182),
                                             self.current_player, 3)

            self.bottom_player.draw(self.screen)
            self.right_player.draw(self.screen)
            self.top_player.draw(self.screen)
            self.left_player.draw(self.screen)

            self.check_button.draw(self.screen)
            self.bet_button.draw(self.screen)
            self.call_button.draw(self.screen)
            self.fold_button.draw(self.screen)

            if self.show_bet_options:
                action_button_x = 50
                action_button_y = 750
                # Draw betting input field
                bet_input_rect = pygame.Rect(action_button_x + 220, action_button_y + 60, 200, 50)
                pygame.draw.rect(self.screen, (255, 255, 255), bet_input_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), bet_input_rect, 2)

                # Draw typed bet text
                font = pygame.font.Font(None, 36)
                bet_text_surface = font.render(self.bet_text, True, (0, 0, 0))
                self.screen.blit(bet_text_surface, (action_button_x + 225, action_button_y + 73))

                # Draw "Confirm", "Cancel", and "All In" buttons
                self.confirm_button.draw(self.screen)
                self.cancel_button.draw(self.screen)
                self.all_in_button.draw(self.screen)

                if self.all_in_button.rect.collidepoint(pygame.mouse.get_pos()):  # Change the logic of All-In later
                    if pygame.mouse.get_pressed()[0]:
                        self.bet_button_clicked = False

            self.screen.blit(self.board.round_text,(520, 400))

            pygame.display.flip()
        except Exception as e:
            print(f"An error occurred: {e}")

    def handle_events(self, event):
        for button in self.action_buttons:
            button.handle_event(event)
            if button.is_clicked():
                if button.text == 'Bet':
                    self.show_bet_options = True
                elif button.text == 'Cancel':
                    self.show_bet_options = False
                    self.bet_text = ""
                elif button.text == 'Confirm':
                    self.send_action_to_server('bet')
                    self.show_bet_options = False
                    self.bet_text = ""
                else:
                    self.send_action_to_server(button.text.lower())
                print(button.text)
        if event.type == pygame.KEYDOWN:
            if self.show_bet_options:
                if event.key == pygame.K_BACKSPACE:
                    self.bet_text = self.bet_text[:-1]
                elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
                                   pygame.K_7, pygame.K_8, pygame.K_9]:
                    typed_number = int(self.bet_text + event.unicode)
                    if typed_number <= self.players[0].money:
                        self.bet_text += event.unicode

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            Thread(target=self.update_game_state).start()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_events(event)

            self.draw()
            clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
