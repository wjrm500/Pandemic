from objects import Card, City, InfectionRateMarker, Player, OutbreakMarker, final_comma_ampersand
import random
import pandas as pd
import time
from operator import attrgetter
import sys

class Game():
    def __init__(self, players, difficulty = "Introductory"):
        self.sleep_secs = 0.05
        self.outbreak_marker = OutbreakMarker()
        time.sleep(self.sleep_secs)
        self.infection_rate_marker = InfectionRateMarker()
        time.sleep(self.sleep_secs)

        ### Load disease cure statuses

        self.disease_cures = {
            "Black": False,
            "Blue": False,
            "Red": False,
            "Yellow": False
        }

        ### Load disease cubes

        num_cubes_per_colour = 24
        self.disease_cubes = {
            "Black": num_cubes_per_colour,
            "Blue": num_cubes_per_colour,
            "Red": num_cubes_per_colour,
            "Yellow": num_cubes_per_colour
        }
        print("Loading {} disease cubes...".format(num_cubes_per_colour * 4))
        time.sleep(self.sleep_secs)

        ### Load cities

        csv_to_read = "pandemic_cities.csv"
        cities_df = pd.read_csv(csv_to_read)
        self.cities = {}
        for index, row in cities_df.iterrows():
            adj = []
            for i in row.iloc[2:8]:
                if pd.notnull(i):
                    adj.append(i)
            city_name = row["City"]
            city_object = City(name = row["City"], colour = row["Colour"], adjacents = adj)
            self.cities.update({city_name: city_object})
        print("Loading {} cities from '{}'...".format(len(self.cities), csv_to_read))
        time.sleep(self.sleep_secs)

        ### Populating cities' adjacent cities lists with city objects

        for city in self.cities.values():
            adjacents = city.adjacents
            adjacent_objects = []
            for adjacent in adjacents:
                adjacent_objects.append(self.cities.get(adjacent))
            city.adjacents = adjacent_objects

        ### Load player and infection decks

        self.player_cards, self.player_discards = [], []
        self.infection_cards, self.infection_discards = [], []
        for city in self.cities.values():
            self.player_cards.append(Card.PlayerCard(city))
            self.infection_cards.append(Card.InfectionCard(city))
        random.shuffle(self.player_cards)
        print("Loading and shuffling {} player cards...".format(len(self.player_cards)))
        time.sleep(self.sleep_secs)
        random.shuffle(self.infection_cards)
        print("Loading and shuffling {} infection cards...".format(len(self.infection_cards)))
        time.sleep(self.sleep_secs)

        ### Check number of and load players

        self.players = []
        if len(players) >= 2 and len(players) <= 4:
            for player in players:
                self.players.append(Player(player))
        else:
            raise ValueError("Number of players must be between 2 and 4!")
        player_names = [player.name for player in self.players]
        print("Loading {} players: {}...".format(len(self.players), ", ".join(player_names)))
        time.sleep(self.sleep_secs)

        ### Deal player cards to players

        for player in self.players:
            cards_per_player = 6 - len(self.players)
            for i in range(cards_per_player):
                player_card = self.player_cards.pop()
                player.hand.update({player_card.city.name: player_card})
        print("Dealing {} player cards each to players...".format(cards_per_player))
        time.sleep(self.sleep_secs)

        ### Assign roles to players

        possible_roles = [
            # "Contingency Planner",
            # "Dispatcher",
            "Medic",
            "Operations Expert",
            "Quarantine Specialist",
            "Researcher",
            "Scientist",
        ]
        role_objects = []
        for role in possible_roles:
            role_objects.append(Card.RoleCard(role))
        random.shuffle(role_objects)
        self.roles = role_objects
        for player in self.players:
            player.role = self.roles.pop()

        ### Setting home city

        home_city = "Atlanta"
        self.home_city = self.cities.get(home_city)
        self.home_city.add_station()
        print("Setting home city to {}...".format(home_city))
        time.sleep(self.sleep_secs)

        ### Move players to Home City (Atlanta)

        for player in self.players:
            player.location = self.home_city
        print("Moving all players to {}...".format(home_city))
        time.sleep(self.sleep_secs)

        ### Check difficulty is valid and prep epidemic cards

        self.epidemic_cards = []
        possible_difficulties = ["Introductory", "Normal", "Heroic"]
        if difficulty in possible_difficulties:
            self.difficulty = difficulty
            if difficulty == "Introductory":
                for i in range(4):
                    self.epidemic_cards.append(Card.EpidemicCard())
            elif difficulty == "Normal":
                for i in range(5):
                    self.epidemic_cards.append(Card.EpidemicCard())
            elif difficulty == "Heroic":
                for i in range(6):
                    self.epidemic_cards.append(Card.EpidemicCard())
        else:
            raise ValueError("Difficulty must be a value from {}".format(possible_difficulties))
        num_epidemics = len(self.epidemic_cards)
        print("Loading {} epidemic cards...".format(num_epidemics))
        time.sleep(self.sleep_secs)

        ### Shuffle in epidemics

        piles = []
        pile_size = len(self.player_cards) // num_epidemics
        remaining_cards = len(self.player_cards) % num_epidemics
        for i in range(num_epidemics):
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
        print("Shuffling epidemic cards into player cards...")
        time.sleep(self.sleep_secs)

        ### Place initial disease cubes

        for i in reversed(range(9)):
            card_to_infect = self.infection_cards.pop()
            cube_colour = card_to_infect.city.colour
            self.disease_cubes[cube_colour] -= 3
            cubes_to_place = (i // 3) + 1
            for j in range(cubes_to_place):
                card_to_infect.city.add_cube(cube_colour, self)
            self.infection_discards.append(card_to_infect)
            cube_cubes = "cube" if cubes_to_place == 1 else "cubes"
            print("Adding {} {} {} to {}...".format(cubes_to_place, card_to_infect.city.colour.lower(), cube_cubes, card_to_infect.city.name))
            time.sleep(self.sleep_secs)

        print("")
        print("Starting game...")
        print("")
        time.sleep(self.sleep_secs * 5)
        for i in range(2):
            print("-" * 50)
        print("")

    def view_play_state(self):
        print("")
        print("-" * 50)
        print("-" * 50)
        print("THE STATE OF PLAY")
        print("-" * 50)
        print("-" * 50)
        print("")
        irm = self.infection_rate_marker
        print("Infection rate marker at position {}/{} - 2 infection cards drawn per 'infect cities' event".format(irm.ir_index + 1, len(irm.ir_hierarchy), irm.infection_rate))
        om = self.outbreak_marker
        print("Outbreak marker at position {}/{} - {} outbreaks until it's game over!".format(om.position + 1, om.limit, om.limit - (om.position + 1)))

        cards_in_discard_pile = final_comma_ampersand([card.city.name for card in self.player_discards])
        card_cards = "card" if len(self.player_discards) == 1 else "cards"
        print("{} {} in the player discard pile {} {}".format(len(self.player_discards), card_cards, "-" if len(self.player_discards) > 0 else "", cards_in_discard_pile))

        cards_in_discard_pile = final_comma_ampersand([card.city.name for card in self.infection_discards])
        card_cards = "card" if len(self.infection_discards) == 1 else "cards"
        print("{} {} in the infection discard pile - {}".format(len(self.infection_discards), card_cards, cards_in_discard_pile))

        print("")
        print("Player locations")
        print("-" * 50)
        for player in self.players:
            print("{} - {}".format(player.name, player.location.name))

        print("")
        print("Disease cure statuses")
        print("-" * 50)
        for key, value in self.disease_cures.items():
            print("{} - {}".format(key, value))

        print("")
        print("Infected cities")
        print("-" * 50)
        previous_colour = ""
        for city in sorted(self.cities.values(), key = attrgetter("colour", "name")):
            colour = city.colour
            if colour != previous_colour:
                # if previous_colour != "":
                    # print("")
                print(city.colour)
                # print("")
            if city.num_cubes > 0:
                cube_cubes = "cube" if city.num_cubes == 1 else "cubes"
                print("  {} - {} {}".format(city.name, city.num_cubes, cube_cubes))
            previous_colour = city.colour


    def go(self):
        while True:
            for player in self.players:
                player.welcome()
                input("Press enter when you are ready {}!\n".format(player.name))
                num_turns = 4
                while num_turns > 0:
                    self.outbroken_cities =  []
                    action_actions = "action" if num_turns == 1 else "actions"
                    print("{} {} remaining!".format(num_turns, action_actions))
                    print("")
                    input("Press enter to take a turn...\n")
                    print("You are in {} ({} x; {} y; {} z)".format(player.location.name, player.location.num_cubes, player.location.num_adjacent_cubes, player.location.get_inner_adjacent_cubes()))
                    cards_in_hand = final_comma_ampersand(["{} ({})".format(city_name, card_object.city.colour) for city_name, card_object in player.hand.items()])
                    print("Your hand contains {}.".format(cards_in_hand))
                    selection = player.show_options(self)
                    if selection["action_type"] == "ferry":
                        player.ferry(selection["end_point"])
                        num_turns -= 1
                    elif selection["action_type"] == "direct_flight":
                        player.direct_flight(selection["end_point"], self)
                        num_turns -= 1
                    elif selection["action_type"] == "charter_flight":
                        player.charter_flight(selection["end_point"], self)
                        num_turns -= 1
                    elif selection["action_type"] == "remove_cube":
                        player.remove_cube(selection["city"], selection["colour"])
                        num_turns -= 1
                    elif selection["action_type"] == "add_station":
                        player.add_station(selection["city"], self)
                        num_turns -= 1
                    elif selection["action_type"] == "cure_disease":
                        player.cure_disease(selection["colour"], self)
                        num_turns -= 1
                    elif selection["action_type"] == "view_play_state":
                        self.view_play_state()
                    elif selection["action_type"] == "do_nothing":
                        num_turns -= 1
                    time.sleep(self.sleep_secs * 10)
                    print("")
                input("Press enter to draw two cards from the player deck...\n")
                player.draw_player_cards(self)
                input("Press enter to infect {} cities...\n".format(self.infection_rate_marker.infection_rate))
                player.infect_cities(self)
                time.sleep(self.sleep_secs * 10)
                print("")
                for i in range(2):
                    print("-" * 50)
                print("")

    def end_game(self):
        print("Game over!")
        time.sleep(5)
        sys.exit()

    def win_game(self):
        print("You won!")
        time.sleep(5)
        sys.exit()
