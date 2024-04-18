import pygame
import sys
import random
import socket
from socketing import Socketing
from server import *


class ClientSocketing:
    def __init__(self, server_address):
        self.server_address = server_address
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.client_socket.connect(self.server_address)
            print("Connected to the server.")
            # Send data to the server
            message = "Hello, server!"
            self.client_socket.sendall(message.encode())
            # Receive data from the server
            data = self.client_socket.recv(1024)
            print("Received:", data.decode())
        finally:
            # Close the connection
            self.client_socket.close()
# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (95, 2, 31)
GREEN = (48, 104, 68)

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Poker Game Selection")

# Create buttons
button_font = pygame.font.Font(None, 28)

# Function to draw rounded rectangle
def draw_rounded_rect(surface, rect, color, radius):
    pygame.draw.circle(surface, color, (rect.left + radius, rect.top + radius), radius)
    pygame.draw.circle(surface, color, (rect.right - radius, rect.top + radius), radius)
    pygame.draw.circle(surface, color, (rect.left + radius, rect.bottom - radius), radius)
    pygame.draw.circle(surface, color, (rect.right - radius, rect.bottom - radius), radius)
    pygame.draw.rect(surface, color, (rect.left + radius, rect.top, rect.width - 2 * radius, rect.height))
    pygame.draw.rect(surface, color, (rect.left, rect.top + radius, rect.width, rect.height - 2 * radius))

# Move buttons to the bottom center
button_0 = pygame.Rect(screen_width // 2 - 75, screen_height - 100, 150, 40)
button_200 = pygame.Rect(screen_width // 2 - 75, screen_height - 200, 150, 40)
button_1600 = pygame.Rect(screen_width // 2 - 75, screen_height - 300, 150, 40)

# Load cloud image as the background
cloud_background = pygame.image.load(r'F:\t\Downloads\10218915.jpg')  # Replace with your actual image file
cloud_background = pygame.transform.scale(cloud_background, (screen_width, screen_height))  # Adjust size as needed

# Initialize player queue
player_queue = []

# Run the game loop
while True:
    # Draw cloud background
    screen.blit(cloud_background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_0.collidepoint(event.pos):
                # Add player to the queue
                player_queue.append("Player 1")

            elif button_200.collidepoint(event.pos):
                # Add player to the queue
                player_queue.append("Player 2")

            elif button_1600.collidepoint(event.pos):
                # Add player to the queue
                player_queue.append("Player 3")

            # Check if the queue has 4 players
            if len(player_queue) == 4:
                # Transition to the poker game screen
                print("Transitioning to Poker Game Screen with Players:", player_queue)
                # Clear the queue for the next round
                player_queue = []

    # Draw rounded buttons
    draw_rounded_rect(screen, button_0, RED, 15)
    draw_rounded_rect(screen, button_200, RED, 15)
    draw_rounded_rect(screen, button_1600, RED, 15)

    # Add custom text to buttons with green color
    text_0 = button_font.render("Cost $0", True, GREEN)
    text_200 = button_font.render("Cost $200", True, GREEN)
    text_1600 = button_font.render("Cost $1600", True, GREEN)

    # Center the text on buttons
    screen.blit(text_0, (button_0.centerx - text_0.get_width() // 2, button_0.centery - text_0.get_height() // 2))
    screen.blit(text_200, (button_200.centerx - text_200.get_width() // 2, button_200.centery - text_200.get_height() // 2))
    screen.blit(text_1600, (button_1600.centerx - text_1600.get_width() // 2, button_1600.centery - text_1600.get_height() // 2))

    pygame.display.flip()
    pygame.time.Clock().tick(10)  # Adjust the frame rate as needed

if __name__ == "__main__":
    # Server address
    server_address = ('127.0.0.1', 68)

    Socketing = Socketing(server_address)
    Socketing.connect_to_server()


