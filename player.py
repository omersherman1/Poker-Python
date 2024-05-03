import json
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.money = 10000
        self.bet = 0
        self.current_best_combination = None
        self.current_score= 0


    def draw_hand(self, deck):
        self.hand = [deck.draw_card() for _ in range(2)]

    def combination(self, card1, card2, arr):
        arr.append(card1)
        arr.append(card2)
        arr_number = []

        pair1 = 0
        pair2 = 0
        three = 0
        four = 0
        flash = 0
        stright = 0
        high_card1 = 0
        high_card2= 0

        for i in range(13):
            arr_number[i] = 0
        for i in range(13):
            for card in arr:
                if card.rank == 'J' and i == 9:
                    arr_number[9]+=1
                if card.rank == 'Q' and i == 10:
                    arr_number[10]+=1
                if card.rank == 'K' and i == 11:
                    arr_number[11]+=1
                if card.rank == 'A' and i == 12:
                    arr_number[12]+=1
                else:
                    if int(card.rank) == i + 2:
                        arr_number[i]+=1
        for i in range(13):
            number = i + 2
            if arr_number[i] == 2:
                if pair1 == 0:
                    pair1 = number
                elif pair2 == 0:
                    pair2 = number
                else:
                    if number > pair1 and number > pair2:
                        if pair1 < pair2:
                            pair1 = number
                        else:
                            pair2 = number
                    elif number > pair1:
                        pair1 = number
                    else:
                        pair2 = number

            elif arr_number[i] == 3:
                if three == 0:
                    three = number
                elif number > three:
                    three = number
            elif arr_number[i] == 4:
                if three == 0:
                    four = number
            elif arr_number[i] == 1 and high_card1 != 0:
                high_card2= high_card1
                high_card1 = arr_number[i]



        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        suits_counter = [0, 0, 0, 0]
        for card in arr:
            for i in range(4):
                if card.suit == suits[i]:
                    suits_counter+=1
        for i in range(4):
            if suits_counter[i] >= 5:
                flash = suits[i]

        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        rank_arr = []
        rank_arr[0] = -1
        index = 0

        for card in arr:
            if card.rank == 'A':
                rank_arr[0] = 1
                card.rank == 14
            if card.rank == 'K':
                card.rank == 13
            if card.rank == 'Q':
                card.rank == 12
            if card.rank == 'J':
                card.rank == 11
            if card.rank < 9:
                int(card.rank) == i + 2
        for card in arr:
            rank_arr[i + 1] = card.rank
        rank_arr.sort()
        rank_arr = list(set(rank_arr))
        for i in range(len - 1):
            if rank_arr[i] + 1 == rank_arr[i + 1]:
                index+=1
            else:
                index = 0
            if index >= 5:
                stright == rank_arr[i + 1]
        return pair1, pair2, three, four, flush, straight, high_card1, high_card2
    def his_hand(pair1, pair2, three, four, flush, straight, high_card1, high_card2):
        if straight != 0 and flush != 0:
            your_combination= "straight flush"
            score= 8000 + straight
        elif four!=0:
            your_combination= "four"
            score= 700 + four
        elif pair1 != 0 and three != 0:
            your_combination= "full house"
            score= 600 + max(pair1, pair2) + three
        elif flush != 0:
            your_combination= "flush"
            score= 500
        elif straight != 0:
            your_combination= "straight"
            score= 400+ straight
        elif three!=0:
            your_combination= "three"
            score= 300 + three
        elif pair1!= 0 and parir2 != 0:
            your_combination= "2 pairs"
            score= 200 + pair1 + pair2
        elif pair1 != 0:
            your_combination= "pairs"
            score= 100 + pair1
        else:
            your_combination= "high cards"
            score= high_card1 + high_card2* 0.01
        self.current_best_combination = your_combination  # Initialize to None
        self.current_score = score

        return your_combination, score

    def __dict__(self):
        return {
            "name": self.name,
            "money": self.money,
            "bet": self.bet,
            "hand": [card.__dict__() for card in self.hand],
            "combination": self.current_best_combination}



class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __dict__(self):
        return {"rank": self.rank, "suit": self.suit}

class Deck:
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

        self.cards = [Card(suit, rank) for rank in ranks for suit in suits]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()