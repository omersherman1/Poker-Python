import pygame
import sys
from jsonListener import  board_status_data

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

class Board:
    def __init__(self, round_number, current_bet, minimum_bet, current_player, community_cards):
        self.round_number = round_number
        self.current_bet = current_bet
        self.minimum_bet = minimum_bet
        self.current_player = current_player
        self.community_cards = [Card(card["Suit"], card["Rank"]) for card in community_cards]

class Game:
    def __init__(self):
        self.board_status_data = board_status_data
        self.board = self.create_board()
        self.players = self.create_players()
        self.your_name = self.board_status_data["your_name"]

        self.screen_width, self.screen_height = 1920, 1000
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Poker Game")

        self.cloud_background = pygame.image.load(r'clouds.jpg')
        self.cloud_background = pygame.transform.scale(self.cloud_background, (self.screen_width, self.screen_height))

        self.card_image_back = pygame.image.load(r'img_poker\back.png')
        self.card_width, self.card_height = self.card_image_back.get_width(), self.card_image_back.get_height()

        self.table_width = 1300
        self.table_height = 600
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
        for i, card in enumerate(self.board.community_cards):
            x = 600 + i * 150
            y = 430
            self.screen.blit(card.image, (x, y))
        for i, player in enumerate(self.players):
            if i == 0:  # Top
                x = self.table_x + self.table_width // 2 - self.card_width
                y = self.table_y - self.card_height + self.card_height - 20
                self.screen.blit(player.hand[0].image, (x, y))
                self.screen.blit(player.hand[1].image, (x + self.card_width + 15, y))
            elif i == 1:  # Right
                x = self.table_x + self.table_width - self.card_width - 20
                y = self.table_y + self.table_height // 2 - self.card_height // 2
                card1 = pygame.transform.rotate(player.hand[0].image, 90)
                card2 = pygame.transform.rotate(player.hand[1].image, 90)
                self.screen.blit(card1, (x, y - self.card_width // 2))
                self.screen.blit(card2, (x, y + self.card_width // 2 + 20))
            elif i == 2:  # Left
                x = self.table_x - 20
                y = self.table_y + self.table_height // 2 - self.card_height // 2
                card1 = pygame.transform.rotate(player.hand[0].image, -90)
                card2 = pygame.transform.rotate(player.hand[1].image, -90)
                self.screen.blit(card1, (x, y - self.card_width // 2))
                self.screen.blit(card2, (x, y + self.card_width // 2 + 20))
            else:  # Bottom
                x = self.table_x + self.table_width // 2 - self.card_width
                y = self.table_y + self.table_height - self.card_height + 20
                self.screen.blit(player.hand[0].image, (x, y))
                self.screen.blit(player.hand[1].image, (x + self.card_width + 15, y))
        action_button_width = 200
        action_button_height = 50
        action_button_x = 50
        action_button_y = 730
        action_buttons = ["Call", "Bet", "Fold", "Check"]
        for i, button in enumerate(action_buttons):
            pygame.draw.rect(self.screen, (139, 69, 19),
                             (action_button_x, action_button_y + i * (action_button_height + 10), action_button_width, action_button_height),
                             border_radius=10)
            font = pygame.font.Font(None, 36)
            text = font.render(button, True, (255, 255, 255))
            text_rect = text.get_rect(
                center=(action_button_x + action_button_width // 2, action_button_y + i * (action_button_height + 10) + action_button_height // 2))
            self.screen.blit(text, text_rect)
        pygame.display.flip()

    def run(self):
        pygame.init()
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
