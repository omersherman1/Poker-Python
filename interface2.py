import pygame
import sys
import socket
from socketing import Socketing
from server import *



pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (95, 2, 31)
GREEN = (48, 104, 68)
BROWN = (139, 69, 19)

# Set up the screen
screen_width, screen_height = 1920, 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Poker Game ")

# Create buttons
button_font = pygame.font.Font(None, 35)

# Function to draw rounded rectangle with variable radius for each corner
def draw_rounded_rect(surface, rect, color, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
# Define buttons
button_fold = pygame.Rect(screen_width // 5 - 20, screen_height - 50, 200, 50)
button_check = pygame.Rect(screen_width // 5 - 20, screen_height - 120, 200, 50)
button_bet = pygame.Rect(screen_width // 5 - 20, screen_height - 190, 200, 50)
button_call = pygame.Rect(screen_width // 5 - 20, screen_height - 260, 200, 50)
button_allin = pygame.Rect(screen_width // 5 - 20, screen_height - 330, 200, 50)

# Load cloud image as the background
cloud_background = pygame.image.load(r'F:\t\Downloads\10218915.jpg')  # Replace with your actual image file
cloud_background = pygame.transform.scale(cloud_background, (screen_width, screen_height))  # Adjust size as needed

# Load card image
card_image_path = r'F:\img_poker\back.png'  # Replace with your card image file
card_image = pygame.image.load(card_image_path)
card_width, card_height = card_image.get_width(), card_image.get_height()

# Calculate the dimensions and position of the circular poker table
table_width = 1300
table_height = 600
table_x = (screen_width - table_width) // 2
table_y = (screen_height - table_height) // 2
frame_thickness = 10
frame_radius = 150

# Create the poker table surface
table_surface = pygame.Surface((table_width, table_height), pygame.SRCALPHA)
pygame.draw.rect(table_surface, GREEN, (0, 0, table_width, table_height), border_radius=frame_radius)

# Calculate position for the cards
card1_x = screen_width // 2 - card_width // 2 - 75
card1_y = 125
card2_x = screen_width // 2 - card_width // 2 + 35
card2_y = 125

# Create rotated card surfaces
card3 = pygame.transform.rotate(card_image, 90)
card4 = pygame.transform.rotate(card_image, 90)

# Calculate position for card3 and card4
card3_x = 240
card3_y = screen_height // 2 - card_width // 2 - 50
card4_x = 240
card4_y = screen_height // 2 + card_width // 2 - 40

# Create rotated card surfaces for card5 and card6
card5 = pygame.transform.rotate(card_image, -90)
card6 = pygame.transform.rotate(card_image, -90)

# Calculate position for card5 and card6
card5_x = screen_width - 300 - card_width
card5_y = screen_height // 2 - card_width // 2 - 50
card6_x = screen_width - 300 - card_width
card6_y = screen_height // 2 + card_width // 2 - 40

# Game loop
running = True
while running:
    screen.blit(cloud_background, (0, 0))

    # Draw poker table
    screen.blit(table_surface, (table_x, table_y))

    # Draw rounded buttons
    draw_rounded_rect(screen, button_fold, RED, 20)
    draw_rounded_rect(screen, button_check, RED, 20)
    draw_rounded_rect(screen, button_bet, RED, 20)
    draw_rounded_rect(screen, button_call, RED, 20)
    draw_rounded_rect(screen, button_allin, RED, 20)

    # Add custom text to buttons with green color
    text_fold = button_font.render("fold", True, GREEN)
    text_check = button_font.render("check", True, GREEN)
    text_bet = button_font.render("bet", True, GREEN)
    text_call = button_font.render("call", True, GREEN)
    text_allin = button_font.render("all in", True, GREEN)

    # Center the text on buttons
    screen.blit(text_fold, (button_fold.centerx - text_fold.get_width() // 2, button_fold.centery - text_fold.get_height() // 2))
    screen.blit(text_check, (button_check.centerx - text_check.get_width() // 2, button_check.centery - text_check.get_height() // 2))
    screen.blit(text_bet, (button_bet.centerx - text_bet.get_width() // 2, button_bet.centery - text_bet.get_height() // 2))
    screen.blit(text_call, (button_call.centerx - text_call.get_width() // 2, button_call.centery - text_call.get_height() // 2))
    screen.blit(text_allin, (button_allin.centerx - text_allin.get_width() // 2, button_allin.centery - text_allin.get_height() // 2))


    screen.blit(card_image, (card1_x, card1_y))
    screen.blit(card_image, (card2_x, card2_y))
    screen.blit(card3, (card3_x, card3_y))
    screen.blit(card4, (card4_x, card4_y))
    screen.blit(card5, (card5_x, card5_y))
    screen.blit(card6, (card6_x, card6_y))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
