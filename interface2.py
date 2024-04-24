
import json
import requests
import pygame
import sys
from jsonListener import  board_status_data
# Assuming you have some way to retrieve board status data
# For example, you can retrieve it from a JSON file


round_number = board_status_data["Round"]
current_bet = board_status_data["CurrentBet"]
minimum_bet = board_status_data["MinimumBet"]
current_player = board_status_data["CurrentPlayer"]
community_cards = board_status_data["CommunityCards"]
your_name = board_status_data["your_name"]

print("Round_number:", round_number)
print("CurrentBet:", current_bet)
print("MinimumBet:", minimum_bet)
print("CurrentPlayer:", current_player)
print("CommunityCards:", community_cards)

players_data = board_status_data["Players"]

# Loop through the player data and print relevant information
for player in players_data:
    name = player["Name"]
    money = player["Money"]
    bet = player["Bet"]
    if your_name == name:
        for card in player["Hand"]:
            card["isHidden"] = False
    hand = [f"{card['Rank']} {card['Suit']}" for card in player["Hand"]]
    print(f"Player: {name}, Money: {money}, Bet: {bet}, Hand: {hand}")

    player1_card_suit = board_status_data["Players"][0]["Hand"][0]["Suit"]
    print("Player1's first card suit:", player1_card_suit)
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
cloud_background = pygame.image.load(r'clouds.jpg')  # Replace with your actual image file
cloud_background = pygame.transform.scale(cloud_background, (screen_width, screen_height))  # Adjust size as needed

H2 = (r'img_poker\2H.png')
D2 = (r'img_poker\2D.png')
C2 = (r'img_poker\2C.png')
S2 = (r'img_poker\2S.png')

H3 = (r'img_poker\3H.png')
D3 = (r'img_poker\3D.png')
C3 = (r'img_poker\3C.png')
S3 = (r'img_poker\3S.png')

H4 = (r'img_poker\4H.png')
D4 = (r'img_poker\4D.png')
C4 = (r'img_poker\4C.png')
S4 = (r'img_poker\4S.png')

H5 = (r'img_poker\5H.png')
D5 = (r'img_poker\5D.png')
C5 = (r'img_poker\5C.png')
S5 = (r'img_poker\5S.png')

H6 = (r'img_poker\6H.png')
D6 = (r'img_poker\6D.png')
C6 = (r'img_poker\6C.png')
S6 = (r'img_poker\6S.png')

H7 = (r'img_poker\7H.png')
D7 = (r'img_poker\7D.png')
C7 = (r'img_poker\7C.png')
S7 = (r'img_poker\7S.png')

H8 = (r'img_poker\8H.png')
D8 = (r'img_poker\8D.png')
C8 = (r'img_poker\8C.png')
S8 = (r'img_poker\8S.png')

H9 = (r'img_poker\9H.png')
D9 = (r'img_poker\9D.png')
C9 = (r'img_poker\9C.png')
S9 = (r'img_poker\9S.png')

H10 = (r'img_poker\10H.png')
D10 = (r'img_poker\10D.png')
C10 = (r'img_poker\10C.png')
S10 = (r'img_poker\10S.png')

HJ = (r'img_poker\11H.png')
DJ = (r'img_poker\11D.png')
CJ = (r'img_poker\11C.png')
SJ = (r'img_poker\11S.png')

HQ = (r'img_poker\12H.png')
DQ = (r'img_poker\12D.png')
CQ = (r'img_poker\12C.png')
SQ = (r'img_poker\12S.png')

HK = (r'img_poker\13H.png')
DK = (r'img_poker13D.png')
CK = (r'img_poker\13C.png')
SK = (r'img_poker\13S.png')

HA = (r'img_poker\14H.png')
DA = (r'img_poker\14D.png')
CA = (r'img_poker\14C.png')
SA = (r'img_poker\14S.png')

cards_imgs_arr = ([[H2, H3, H4, H5, H6, H7, H8, H9, H10, HJ, HQ, HK, HA],
                   [D2, D3, D4, D5, D6, D7, D8, D9, D10, DJ, DQ, DK, DA],
                   [C2, C3, C4, C5, C6, C7, C8, C9, C10, CJ, CQ, CK, CA],
                   [D2, D3, D4, D5, D6, D7, D8, D9, D10, DJ, DQ, DK, DA]])

# Load card image
card_image_back = (r'img_poker\back.png')  # Replace with your card image file
card_image_back = pygame.image.load(card_image_back)
card_width, card_height = card_image_back.get_width(), card_image_back.get_height()

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

card1 = card_image_back
card2 = card_image_back
# Calculate position for the cards
card1_x = screen_width // 2 - card_width // 2 - 75
card1_y = 125
card2_x = screen_width // 2 - card_width // 2 + 35
card2_y = 125

# Create rotated card surfaces
card3 = pygame.transform.rotate(card_image_back, 90)
card4 = pygame.transform.rotate(card_image_back, 90)

# Calculate position for card3 and card4
card3_x = 240
card3_y = screen_height // 2 - card_width // 2 - 50
card4_x = 240
card4_y = screen_height // 2 + card_width // 2 - 40

# Create rotated card surfaces for card5 and card6
card5 = pygame.transform.rotate(card_image_back, -90)
card6 = pygame.transform.rotate(card_image_back, -90)

# Calculate position for card5 and card6
card5_x = screen_width - 300 - card_width
card5_y = screen_height // 2 - card_width // 2 - 50
card6_x = screen_width - 300 - card_width
card6_y = screen_height // 2 + card_width // 2 - 40

ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

your_name = board_status_data["your_name"]
name_index= int(your_name[6])-1
a1=0
b1=0
a2=0
b2=0
for i in range(4):
    for j in range(13):
        if board_status_data["Players"][name_index]["Hand"][0]["Suit"] == suits[i] and board_status_data["Players"][name_index]["Hand"][0]["Rank"] == ranks[j]:
            a1 = i
            b1 = j
        elif board_status_data["Players"][name_index]["Hand"][1]["Suit"] == suits[i] and board_status_data["Players"][name_index]["Hand"][1]["Rank"] == ranks[j]:
            a2 = i
            b2 = j

hand_card1 = cards_imgs_arr[a1][b1]
hand_card2 = cards_imgs_arr[a2][b2]
hand_card1 = pygame.image.load(hand_card1)
hand_card2 = pygame.image.load(hand_card2)

hand_card1_x = screen_width // 2 - card_width // 2 - 75
hand_card1_y = 720
hand_card2_x = screen_width // 2 - card_width // 2 + 35
hand_card2_y = 720


community_card1 = (card_image_back)
community_card2 = (card_image_back)
community_card3 = (card_image_back)
community_card4 = (card_image_back)
community_card5 = (card_image_back)

community_arr=[community_card1, community_card2, community_card3, community_card4, community_card5]
index_community_cards= 0
for i in range(5):
    if board_status_data["CommunityCards"][i]["isHidden"]!= True:
        index_community_cards= index_community_cards+1

for i in range(index_community_cards):
    for w in range(4):
        for j in range(13):
            if board_status_data["CommunityCards"][i]["Suit"] == suits[w] and board_status_data["CommunityCards"][i]["Rank"] == ranks[j]:
                community_arr[i]= cards_imgs_arr[w][j]

community_card1= community_arr[0]
community_card2= community_arr[1]
community_card3= community_arr[2]
community_card4= community_arr[3]
community_card5= community_arr[4]

if isinstance(community_card1, str):
    community_card1 = pygame.image.load(community_card1)
if isinstance(community_card2, str):
    community_card2 = pygame.image.load(community_card2)
if isinstance(community_card3, str):
    community_card3 = pygame.image.load(community_card3)
if isinstance(community_card4, str):
    community_card4 = pygame.image.load(community_card4)
if isinstance(community_card5, str):
    community_card5 = pygame.image.load(community_card5)







community_card1_x = 600
community_card1_y = 430
community_card2_x = 750
community_card2_y = 430
community_card3_x = 900
community_card3_y = 430
community_card4_x = 1050
community_card4_y = 430
community_card5_x = 1200
community_card5_y = 430







profile1_image = pygame.image.load(r'img_poker\profile1.png')
profile1_image = pygame.transform.scale(profile1_image, (100, 100))
profile1_surface = pygame.Surface((100, 100))
profile1_surface.fill((224, 122, 95))
profile1_surface.blit(profile1_image, (0, 0))
profile1 = profile1_surface.convert_alpha()
screen.blit(profile1, (700, 750))


# Load profile2 image and resize it
profile2_image = pygame.image.load(r'img_poker\profile2.png')
profile2_image = pygame.transform.scale(profile2_image, (100, 100))
profile2_image_rotated = pygame.transform.rotate(profile2_image, 90)
profile2_surface = pygame.Surface((100, 100))
profile2_surface.fill((	135, 206, 235))  # sky blue background
profile2_surface.blit(profile2_image_rotated, (0, 0))
profile2 = profile2_surface.convert_alpha()

profile3_image = pygame.image.load(r'img_poker\profile3.png')
profile3_image = pygame.transform.scale(profile3_image, (100, 100))
profile3_image_rotated = pygame.transform.rotate(profile3_image, 180)
profile3_surface = pygame.Surface((100, 100))
profile3_surface.fill((	111, 78, 55))
profile3_surface.blit(profile3_image_rotated, (0, 0))
profile3 = profile3_surface.convert_alpha()
screen.blit(profile3, (1075, 150))

profile4_image = pygame.image.load(r'img_poker\profile4.png')
profile4_image = pygame.transform.scale(profile4_image, (100, 100))
profile4_image_rotated = pygame.transform.rotate(profile4_image, 270)
profile4_surface = pygame.Surface((100, 100))
profile4_surface.fill((253, 255, 182))
profile4_surface.blit(profile4_image_rotated, (0, 0))
profile4 = profile4_surface.convert_alpha()
screen.blit(profile4, (260,275))

def send_board_status():
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect(('127.0.0.1', 8000))
    packet_data = \
        {
            "Status": "ReadyToGetBoard"
        }
    r = requests.post("http://localhost:8000", data=json.dumps(packet_data))
    print(r.text)
    # s.sendall(bytes(json.dumps(packet_data), encoding="utf-8"))
    # s.close()


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
    screen.blit(text_fold,
                (button_fold.centerx - text_fold.get_width() // 2, button_fold.centery - text_fold.get_height() // 2))
    screen.blit(text_check, (
        button_check.centerx - text_check.get_width() // 2, button_check.centery - text_check.get_height() // 2))
    screen.blit(text_bet,
                (button_bet.centerx - text_bet.get_width() // 2, button_bet.centery - text_bet.get_height() // 2))
    screen.blit(text_call,
                (button_call.centerx - text_call.get_width() // 2, button_call.centery - text_call.get_height() // 2))
    screen.blit(text_allin, (
        button_allin.centerx - text_allin.get_width() // 2, button_allin.centery - text_allin.get_height() // 2))

    screen.blit(card1, (card1_x, card1_y))
    screen.blit(card2, (card2_x, card2_y))
    screen.blit(card3, (card3_x, card3_y))
    screen.blit(card4, (card4_x, card4_y))
    screen.blit(card5, (card5_x, card5_y))
    screen.blit(card6, (card6_x, card6_y))
    screen.blit(hand_card1, (hand_card1_x, hand_card1_y))
    screen.blit(hand_card2, (hand_card2_x, hand_card2_y))
    screen.blit(community_card1, (community_card1_x, community_card1_y))
    screen.blit(community_card2, (community_card2_x, community_card2_y))
    screen.blit(community_card3, (community_card3_x, community_card3_y))
    screen.blit(community_card4, (community_card4_x, community_card4_y))
    screen.blit(community_card5, (community_card5_x, community_card5_y))
    screen.blit(profile1, (700, 750))
    screen.blit(profile2, (1550, 635))
    screen.blit(profile3, (1075, 150))
    screen.blit(profile4, (260,275))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_check.collidepoint(event.pos):
                send_board_status()

    pygame.display.flip()

pygame.quit()
sys.exit()