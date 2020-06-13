import random
import sys
from epidemic_probability import ep_calculator

class Game():
    def __init__(self, players, num_epidemics):
        self.player_cards, self.player_discards = [], []
        for i in range(53):
            self.player_cards.append("city")
        random.shuffle(self.player_cards)

        self.players = []
        for player in players:
            self.players.append(Player())

        for player in self.players:
            cards_per_player = 6 - len(self.players)
            for i in range(cards_per_player):
                player_card = self.player_cards.pop()
                player.hand.append("city")

        self.epidemic_cards = []
        self.num_epidemics = num_epidemics
        self.epidemics_drawn = 0
        for i in range(self.num_epidemics):
            self.epidemic_cards.append("epidemic")

        piles = []
        pile_size = len(self.player_cards) // self.num_epidemics
        remaining_cards = len(self.player_cards) % self.num_epidemics
        for i in range(self.num_epidemics):
            pile = []
            for j in range(pile_size):
                pile.append(self.player_cards.pop())
            pile.append(self.epidemic_cards.pop())
            while remaining_cards > 0:
                pile.append(self.player_cards.pop())
                remaining_cards -= 1
            random.shuffle(pile)
            piles.append(pile)
        self.player_cards = [card for pile in piles for card in pile]

    def go(self):
        while True:
            for player in self.players:
                player.draw_player_cards(self)
                print("")

    def end_game(self):
        print("Game over!")
        sys.exit()

class Player():
    def __init__(self):
        self.hand = []

    def draw_player_cards(self, game):
        cards_to_draw = 2
        for i in range(cards_to_draw):
            cih = {i: len(player.hand) for i, player in enumerate(game.players)}
            ep = ep_calculator(num_players = len(game.players), cards_in_hands = cih, total_epidemics = game.num_epidemics, epidemics_drawn = game.epidemics_drawn, num_player_discards = len(game.player_discards))
            try:
                card = game.player_cards.pop()
            except:
                game.end_game()
            if card == "city":
                self.hand.append("city")
            elif card == "epidemic":
                print("Chance of an epidemic: {}".format(ep))
                print("Card drawn: {}".format(card))
                game.epidemics_drawn += 1
        self.check_num_cards(game)

    def check_num_cards(self, game):
        num_cards_in_hand = len(self.hand)
        max_cards_in_hand = 7
        while num_cards_in_hand > max_cards_in_hand:
            card_to_discard = self.hand.pop()
            game.player_discards.append("city")
            num_cards_in_hand = len(self.hand)

g = Game(["Will", "Kate"], 6)
print(g.go())
