import os
import random
import socket
from threading import Thread
import json.decoder
import pygame
import sys
from collections import deque
import json


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.path = f"img_poker\\{self.suit}{self.rank}.png"
        self.image = pygame.image.load(self.path)


class Status:
    def __init__(self, status):
        self.status = status
        self.font = pygame.font.Font(None, 36)
        self.status_text = self.font.render(f"{self.status}", True, (255, 0, 0))

    def draw(self, screen):
        screen.blit(self.status_text, (520, 615))


class Player:
    def __init__(self, name, money, bet, hand, current_best_combination, profile_path):
        self.name = name
        self.money = money
        self.bet = bet
        self.combination = current_best_combination
        self.hand = [Card(card["suit"], card["rank"]) for card in hand]
        self.profile_path = profile_path
        self.profile = pygame.image.load(self.profile_path)
        self.font = pygame.font.Font(None, 36)
        self.name_text = self.font.render(f"{self.name}", True, (255, 255, 255))
        self.money_text = self.font.render(f"Money: {self.money}", True, (0, 0, 0))
        self.bet_text = self.font.render(f"Bet: {self.bet}", True, (0, 0, 0))
        self.combination_text = self.font.render(f"Your Best Combination: {self.combination}", True, (0, 0, 0))


class Board:
    def __init__(self, round_number, minimum_bet, current_player, community_cards, pot):
        self.round_number = round_number
        self.minimum_bet = minimum_bet
        self.current_player = current_player
        self.community_cards = [Card(card["suit"], card["rank"]) for card in community_cards]
        self.pot = pot

        self.font = pygame.font.Font(None, 36)
        self.round_text = self.font.render(f"Round: {self.round_number}", True, (0, 0, 0))
        self.pot_text = self.font.render(f"Pot: {self.pot}", True, (0, 0, 0))
        self.minimum_bet_text = self.font.render(f"Minimum Bet: {self.minimum_bet}", True, (0, 0, 0))


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
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.clicked = True

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
        self.player = player
        self.x = x
        self.y = y
        self.back_card = back_card
        self.color = color
        self.current_player = current_player
        self.index = index

    def profile_maker(self):
        profile_image = pygame.transform.scale(self.player.profile, (100, 100))
        profile_surface = pygame.Surface((100, 100))
        profile_surface.fill(self.color)
        profile_surface.blit(profile_image, (0, 0))
        return profile_surface.convert_alpha()

    def draw(self, screen):
        card1 = pygame.transform.rotate(self.back_card, self.index * 90)
        card2 = pygame.transform.rotate(self.back_card, self.index * 90)
        screen.blit(self.profile_maker(), (self.x, self.y))

        font = pygame.font.Font(None, 36)
        your_plate = font.render("Your", True, (255, 255, 255))
        his_plate = font.render(f"{self.current_player}'s", True, (255, 255, 255))
        turn_plate = font.render("Turn", True, (255, 255, 255))

        if self.index == 0:
            card1 = pygame.transform.rotate(self.player.hand[0].image, self.index * 90)
            card2 = pygame.transform.rotate(self.player.hand[1].image, self.index * 90)
            screen.blit(card1, (self.x + 55, self.y - 169))
            screen.blit(card2, (self.x - 55, self.y - 169))
            screen.blit(self.player.name_text, (self.x + 170, self.y - 150))
            screen.blit(self.player.money_text, (self.x + 170, self.y - 120))
            screen.blit(self.player.bet_text, (self.x + 170, self.y - 90))
            screen.blit(self.player.combination_text, (self.x - 500, self.y - 100))
            if self.player.name == self.current_player:
                pygame.draw.circle(screen, (160,82,45), (self.x + 200, self.y + 50), 50)
                screen.blit(your_plate, (self.x + 175, self.y + 20))
                screen.blit(turn_plate, (self.x + 175, self.y + 50))
        elif self.index == 1:
            screen.blit(card1, (self.x - 170, self.y + 55))
            screen.blit(card2, (self.x - 170, self.y - 55))
            screen.blit(self.player.name_text, (self.x - 220, self.y - 165))
            screen.blit(self.player.money_text, (self.x - 220, self.y - 135))
            screen.blit(self.player.bet_text, (self.x - 220, self.y - 105))
            if self.player.name == self.current_player:
                pygame.draw.circle(screen, (160,82,45), (self.x + 50, self.y - 100), 50)
                screen.blit(his_plate, (self.x + 22, self.y -125 ))
                screen.blit(turn_plate, (self.x + 25, self.y - 100))
        elif self.index == 2:
            screen.blit(card1, (self.x + 55, self.y + 125))
            screen.blit(card2, (self.x - 55, self.y + 125))
            screen.blit(self.player.name_text, (self.x - 250, self.y + 150))
            screen.blit(self.player.money_text, (self.x - 250, self.y + 180))
            screen.blit(self.player.bet_text, (self.x - 250, self.y + 210))
            if self.player.name == self.current_player:
                pygame.draw.circle(screen, (160,82,45), (self.x - 100, self.y + 50), 50)
                screen.blit(his_plate, (self.x -122 , self.y + 25))
                screen.blit(turn_plate, (self.x -125 , self.y + 50))
        elif self.index == 3:
            screen.blit(card1, (self.x + 128, self.y + 55))
            screen.blit(card2, (self.x + 128, self.y - 55))
            screen.blit(self.player.name_text, (self.x + 170, self.y - 165))
            screen.blit(self.player.money_text, (self.x + 170, self.y - 135))
            screen.blit(self.player.bet_text, (self.x + 170, self.y - 105))
            if self.player.name == self.current_player:
                pygame.draw.circle(screen, (160,82,45), (self.x + 50, self.y + 160), 50)
                screen.blit(his_plate, (self.x + 22, self.y + 135))
                screen.blit(turn_plate, (self.x + 25, self.y + 160))



class Game:
    def __init__(self):
        pygame.init()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()
        self.player_name = ''
        self.is_before_login = True
        self.game_started = False

        self.board = None
        self.players = None
        self.current_player = None
        self.message = None

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

        self.login_button = Button(850, 525, 200, 50, "Login", action_button_color)

        self.action_buttons = [self.check_button, self.bet_button, self.call_button, self.fold_button,
                               self.confirm_button, self.cancel_button, self.all_in_button, self.login_button]

        self.screen_width = 1920
        self.screen_height = 1000
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Poker Game")

        self.cloud_background = pygame.transform.scale(pygame.image.load(r'clouds.jpg'),
                                                       (self.screen_width, self.screen_height))
        self.last_bet_amount = 0
        self.bet_amount = 0
        self.bet_text = ''
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
            print(self.bet_text)
            json_data['bet'] = int(self.bet_text)
        self.socket.sendall(json.dumps(json_data).encode())

    def send_name_to_server(self):
        json_data = {"Player Name": self.player_name}
        print(json_data)
        self.socket.sendall(json.dumps(json_data).encode())

    def update_game_state(self):
        while True:
            response = self.socket.recv(1024).decode()
            print(response)
            if response:
                self.board_status_data = json.loads(response)
                self.board = self.create_board()
                self.players = self.create_players()
                self.message = self.create_status()
                self.current_player = self.board_status_data["Current Player"]
                self.game_started = True

    def create_board(self):
        round_number = self.board_status_data["Round"]
        minimum_bet = self.board_status_data["Minimum Bet"]
        current_player = self.board_status_data["Current Player"]
        community_cards = self.board_status_data["Community Cards"]
        pot = self.board_status_data["Pot"]

        return Board(round_number, minimum_bet, current_player, community_cards, pot)

    def create_status(self):
        status = self.board_status_data["Status"]
        return Status(status)

    def create_players(self):
        players_data = self.board_status_data["Players"]
        return [(Player(player["name"], player["money"], player["bet"], player["hand"], player["combination"], player["profile_path"])) for
                player in players_data]

    def draw_login_screen(self):
        self.screen.blit(self.cloud_background, (0, 0))  # Draw cloud image as background

        rect = pygame.Rect(800, 400, 300, 200)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, border_radius=15)
        font = pygame.font.Font(None, 45)
        text_surface = font.render("Enter your name:", True, (255, 255, 255))
        self.screen.blit(text_surface, (830, 410))

        player_name_input = pygame.Rect(850, 450, 200, 50)
        player_name_surface = font.render(self.player_name, True, (0, 0, 0))

        pygame.draw.rect(self.screen, (255, 255, 255), player_name_input)
        pygame.draw.rect(self.screen, (0, 0, 0), player_name_input, 2)
        self.screen.blit(player_name_surface, (860, 460))

        self.login_button.draw(self.screen)

    def draw_waiting_screen(self):
        self.screen.blit(self.cloud_background, (0, 0))  # Draw cloud image as background

        rect = pygame.Rect(800, 400, 300, 200)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, border_radius=15)
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render("Waiting For Server...", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

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

            while players_queue[0].name != self.player_name:
                players_queue.append(players_queue.popleft())

            self.bottom_player = PlayerProfile(players_queue[0], 920, 850, self.card_image_back, (0, 0, 128),
                                               self.current_player, 0)
            self.right_player = PlayerProfile(players_queue[1], 1711, 452, self.card_image_back, (135, 206, 235),
                                              self.current_player, 1)
            self.top_player = PlayerProfile(players_queue[2], 920, 50, self.card_image_back, (111, 78, 55),
                                            self.current_player, 2)
            self.left_player = PlayerProfile(players_queue[3], 108, 452, self.card_image_back, (253, 255, 182),
                                             self.current_player, 3)

            self.bottom_player.draw(self.screen)
            self.right_player.draw(self.screen)
            self.top_player.draw(self.screen)
            self.left_player.draw(self.screen)

            if self.message.status is not None:
                if self.current_player == self.player_name:
                    self.message.draw(self.screen)

            if self.current_player == self.player_name:
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

            self.screen.blit(self.board.round_text, (520, 370))
            self.screen.blit(self.board.pot_text, (520, 400))
            self.screen.blit(self.board.minimum_bet_text, (520, 585))

            pygame.display.flip()

        except Exception as e:
            print(f"An error occurred: {e}")

    def handle_events(self, event):
        for button in self.action_buttons:
            button.handle_event(event)
            if button.is_clicked():
                if button.text == 'Bet':
                    if self.current_player == self.player_name:
                        self.show_bet_options = True
                elif button.text == 'Cancel':
                    self.show_bet_options = False
                    self.bet_text = ''
                elif button.text == 'Confirm':
                    self.send_action_to_server('bet')
                    self.show_bet_options = False
                    self.bet_text = ''
                elif button.text == 'All In':
                    for player in self.players:
                        if self.current_player == player.name:
                            self.bet_text = player.money
                    self.send_action_to_server('bet')
                    self.show_bet_options = False
                    self.bet_text = ''
                elif button.text == 'Login':
                    self.send_name_to_server()
                    self.is_before_login = False
                else:
                    self.send_action_to_server(button.text.lower())

                button.clicked = False
        if event.type == pygame.KEYDOWN:
            if self.show_bet_options:
                if event.key == pygame.K_BACKSPACE:
                    self.bet_text = self.bet_text[:-1]
                elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
                                   pygame.K_7, pygame.K_8, pygame.K_9]:
                    typed_number = int(self.bet_text + event.unicode)
                    if typed_number <= self.players[0].money:
                        self.bet_text += event.unicode

            elif self.is_before_login:
                if event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    self.player_name += event.unicode

    def run(self):
        clock = pygame.time.Clock()
        running = True

        Thread(target=self.update_game_state).start()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_events(event)

            if self.is_before_login:
                self.draw_login_screen()
            elif not self.game_started:
                self.draw_waiting_screen()
            else:
                self.draw()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()

