import time
import random

class Player():
    def __init__(self, name):
        self.name = name
        self.role = ""
        self.location = ""
        self.hand = {}
        self.ready_to_cure = False
        self.cure_colour = ""

    def check_for_cure(self, game):
        colours = []
        for key, value in game.disease_cures.items():
            if value == False:
                colours.append(key)
        for colour in colours:
            colour_cards = 0
            for card in self.hand.values():
                if card.city.colour == colour:
                    colour_cards += 1
                    if colour_cards == 3:
                        self.ready_to_cure = True
                        self.cure_colour = colour
                        break

    def welcome(self):
        print("Hi {}!\n".format(self.name))

    def show_options(self, game):
        print("What would you like to do?")
        print("")
        time.sleep(game.sleep_secs * 2)
        x, y, dod = 1, "", {}
        for adjacent in self.location.adjacents:
            d = {
                "action_type": "ferry",
                "end_point": adjacent,
                "text": "Ferry to {} ({} x; {} y; {} z)".format(adjacent.name, adjacent.num_cubes, adjacent.num_adjacent_cubes, adjacent.get_inner_adjacent_cubes())
            }
            print(str(x) + ". " + d.get("text"))
            dod.update({x: d})
            x += 1
            time.sleep(game.sleep_secs)
        print("")
        for card in self.hand.values():
            if card.city != self.location:
                d = {
                    "action_type": "direct_flight",
                    "end_point": card.city,
                    "text": "Direct flight to {} ({} x; {} y; {} z)".format(card.city.name, card.city.num_cubes, card.city.num_adjacent_cubes, card.city.get_inner_adjacent_cubes())
                }
                print(str(x) + ". " + d.get("text"))
                dod.update({x: d})
                x += 1
                time.sleep(game.sleep_secs)
        print("")
        for card in self.hand.values():
            if card.city == self.location:
                d = {
                    "action_type": "charter_flight",
                    "end_point": "",
                    "text": "Charter flight to any city"
                }
                print(str(x) + ". " + d.get("text"))
                dod.update({x: d})
                y = x ### For tracking the index of chartered flight option
                x += 1
                time.sleep(game.sleep_secs)
                print("")
                if self.location.station == False:
                    d = {
                        "action_type": "add_station",
                        "city": card.city,
                        "text": "Add a research station to {}".format(card.city.name)
                    }
                    print(str(x) + ". " + d.get("text"))
                    dod.update({x: d})
                    x += 1
                    time.sleep(game.sleep_secs)
                    print("")
        for i in self.location.cubes:
            if self.location.cubes.get(i) > 0:
                d = {
                    "action_type": "remove_cube",
                    "city": self.location,
                    "colour": i,
                    "text": "Remove 1 {} disease cube from {}".format(i.lower(), self.location.name)
                }
                print(str(x) + ". " + d.get("text"))
                dod.update({x: d})
                x += 1
                time.sleep(game.sleep_secs)
                print("")
        self.check_for_cure(game)
        if self.location.station == True and self.ready_to_cure == True:
            d = {
                "action_type": "cure_disease",
                "colour": self.cure_colour,
                "text": "Cure {} disease".format(self.cure_colour.lower())
            }
            print(str(x) + ". " + d.get("text"))
            dod.update({x: d})
            x += 1
            time.sleep(game.sleep_secs)
            print("")

        d = {
            "action_type": "view_play_state",
            "text": "View state of play"
        }
        print(str(x) + ". " + d.get("text"))
        dod.update({x: d})
        x += 1
        time.sleep(game.sleep_secs)
        print("")

        d = {
            "action_type": "do_nothing",
            "text": "... Or you could just pass (do nothing)!"
        }
        print(str(x) + ". " + d.get("text"))
        dod.update({x: d})
        time.sleep(game.sleep_secs)
        print("")
        while True:
            try:
                selection = int(input("Which option do you wish to select?\n"))
                if selection > x:
                    raise ValueError("Your input was out of bounds.")
            except ValueError:
                print("You did not enter a valid option. Please try again.")
            else:
                break
        print("")

        if selection == y: ### If charter flight selected
            ### Find city with most cubes / most adjacent cubes
            print("Suggested options below...")
            print("")
            charterabilities = {}
            for city in game.cities.values():
                charterability = city.num_cubes + (city.num_adjacent_cubes / 2) + (city.num_inner_adjacent_cubes / 4)
                if len(charterabilities) < 3:
                    charterabilities.update({city.name: charterability})
                else:
                    if charterability > min(charterabilities.values()):
                        popper = min(charterabilities, key = charterabilities.get)
                        charterabilities.pop(popper)
                        charterabilities.update({city.name: charterability})
            while len(charterabilities) > 0:
                city_key = max(charterabilities, key = charterabilities.get)
                del charterabilities[city_key]
                print("{} ({} x; {} y; {} z)".format(city_key, game.cities.get(city_key).num_cubes, game.cities.get(city_key).num_adjacent_cubes, game.cities.get(city_key).get_inner_adjacent_cubes()))
            print("")
            while True:
                try:
                    cf_selection = input("Input a valid city for your chartered flight:\n")
                    city_object = game.cities.get(cf_selection)
                    if city_object not in game.cities.values() or city_object == self.location:
                        raise ValueError()
                    dod[y]["end_point"] = city_object
                except ValueError:
                    print("You did not enter a valid city. Please try again.")
                else:
                    break
        else:
            print("You selected '{}'.".format(dod.get(selection).get("text")))
            time.sleep(game.sleep_secs * 5)
        return dod.get(selection)

    def show_hand(self):
        cards_in_hand = []
        for card in self.hand.values():
            cards_in_hand.append(card.city.name)
        print("{}'s hand contains {}.".format(self.name, ", ".join(cards_in_hand)))

    ### Turn actions

    def ferry(self, end_point):
        print("{} ferried from {} to {}.".format(self.name, self.location.name, end_point.name))
        self.location = end_point

    def direct_flight(self, end_point, game):
        print("{} took a direct flight from {} to {}.".format(self.name, self.location.name, end_point.name))
        self.location = end_point
        card_to_discard = self.hand.pop(end_point.name)
        game.player_discards.append(card_to_discard)

    def charter_flight(self, end_point, game):
        print("{} took a charter flight from {} to {}.".format(self.name, self.location.name, end_point.name))
        card_to_discard = self.hand.pop(self.location.name)
        game.player_discards.append(card_to_discard)
        self.location = end_point
        ### Need to add removed card to discard pile

    def remove_cube(self, city, colour = ""):
        colour = city.colour
        print("{} removed a {} disease cube from {}.".format(self.name, colour.lower(), city.name))
        city.cubes[colour] -= 1
        city.num_cubes -= 1
        for adjacent in city.adjacents:
            adjacent.num_adjacent_cubes -= 1

    def add_station(self, city, game):
        print("{} added a research station to {}.".format(self.name, city.name))
        city.add_station()
        card_to_discard = self.hand.pop(city.name)
        game.player_discards.append(card_to_discard)

    def cure_disease(self, colour, game):
        card_city_names = []
        for card in self.hand.values():
            if card.city.colour == colour:
                card_city_names.append(card.city.name)
        for i in card_city_names:
            card_to_discard = self.hand.pop(i)
            game.player_discards.append(card_to_discard)
        game.disease_cures[colour] = True
        print("{} cured the {} disease.".format(self.name, colour.lower()))
        if all(game.disease_cures.values()):
            game.win_game()
        self.ready_to_cure = False

    # def share_knowledge(self, card, other_player, game):
    #     card_to_share = self.hand.pop(card)
    #     other_player.hand.update({card: card_to_share})
    #     other_player.check_num_cards(game)
    #
    # def take_knowledge(self, )

    ### Draw 2 player cards to add to hand

    def draw_player_cards(self, game):
        cards_to_draw = 2
        for i in range(cards_to_draw):
            try:
                card = game.player_cards.pop()
            except:
                game.end_game()

            if isinstance(card, Card.PlayerCard):
                self.hand.update({card.city.name: card})
                print("{} picked up {}.".format(self.name, card.city.name))
                time.sleep(game.sleep_secs)
            elif isinstance(card, Card.EpidemicCard):
                ### 1. Increase
                input("You picked up an epidemic card! Press enter to increase the infection rate...\n")
                previous_infection_rate = game.infection_rate_marker.infection_rate
                game.infection_rate_marker.increase()
                print("Infection rate increased from {} to {}.".format(previous_infection_rate, game.infection_rate_marker.infection_rate))
                print("")
                time.sleep(game.sleep_secs)
                ### 2. Infect
                input("Press enter to infect a completely new city with 3 cubes...\n")
                card_to_infect = game.infection_cards.pop(1)
                cube_colour = card_to_infect.city.colour
                game.disease_cubes[cube_colour] -= 3
                for i in range(3):
                    card_to_infect.city.add_cube(cube_colour, game)
                print("{} hit {} with an epidemic!".format(self.name, card_to_infect.city.name))
                print("")
                time.sleep(game.sleep_secs)
                ### 3. Intensify
                input("Press enter to shuffle the infection discard pile and add it to the top of the infection deck...\n")
                random.shuffle(game.infection_discards)
                game.infection_cards.extend(game.infection_discards)
                print("{} grimaced as they shuffled the infection discard pile and added it to the top of the infection deck.".format(self.name))
                time.sleep(game.sleep_secs)
        print("")
        self.check_num_cards(game)

    def check_num_cards(self, game):
        num_cards_in_hand = len(self.hand)
        max_cards_in_hand = 7
        while num_cards_in_hand > max_cards_in_hand:
            # cards_in_hand = final_comma_ampersand([card for card in self.hand.keys()])
            cards_in_hand = final_comma_ampersand(["{} ({})".format(city_name, card_object.city.colour) for city_name, card_object in self.hand.items()])
            while True:
                try:
                    card_to_discard = input("You have {} cards in your hand: {}. Please choose one to discard.\n".format(num_cards_in_hand, cards_in_hand))
                    if card_to_discard not in self.hand:
                        raise ValueError()
                    card_to_discard = self.hand.pop(card_to_discard)
                    game.player_discards.append(card_to_discard)
                    num_cards_in_hand = len(self.hand)
                    print("{} discarded.".format(card_to_discard.city.name))
                except ValueError:
                    print("You did not enter a valid city. Please try again.")
                else:
                    break

    def infect_cities(self, game):
        for i in range(game.infection_rate_marker.infection_rate):
            card_to_infect = game.infection_cards.pop()
            print("{} infected {}.".format(self.name, card_to_infect.city.name))
            cube_cubes = "cube" if card_to_infect.city.num_cubes + 1 == 1 else "cubes"
            if card_to_infect.city.num_cubes + 1 <= 3:
                print("{} now has {} disease {}.".format(card_to_infect.city.name, card_to_infect.city.num_cubes + 1, cube_cubes))
                print("")
            card_to_infect.city.add_cube(card_to_infect.city.colour, game)
            time.sleep(game.sleep_secs)

class City():
    def __init__(self, name, colour, adjacents):
        self.name = name
        self.colour = colour
        self.adjacents = adjacents
        self.cubes = {
            "Black": 0,
            "Blue": 0,
            "Red": 0,
            "Yellow": 0
        }
        self.num_cubes = 0
        self.num_adjacent_cubes = 0
        self.num_inner_adjacent_cubes = 0
        self.station = False

    def add_cube(self, colour, game):
        if self.num_cubes < 3:
            self.cubes[colour] += 1
            self.num_cubes += 1
            try:
                game.disease_cubes[colour] -= 1
            except:
                game.end_game()
            for adjacent in self.adjacents:
                adjacent.num_adjacent_cubes += 1
        else:
            if self in game.outbroken_cities:
                pass
            else:
                self.outbreak(game)

    def add_station(self):
        self.station = True

    def outbreak(self, game):
        game.outbroken_cities.append(self)
        adjacent_city_names = []
        for adjacent in self.adjacents:
            adjacent_city_names.append(adjacent.name)
        adjacent_city_names = final_comma_ampersand(adjacent_city_names)
        print("{} suffered an outbreak! {} were collateral damage.".format(self.name, adjacent_city_names))
        game.outbreak_marker.increase(game)
        for adjacent in self.adjacents:
            adjacent.add_cube(self.colour, game)
            cube_cubes = "cube" if adjacent.num_cubes == 1 else "cubes"
            print("{} now has {} disease {}.".format(adjacent.name, adjacent.num_cubes, cube_cubes))
        print("")

    def get_inner_adjacent_cubes(self):
        num_inner_adjacent_cubes = 0
        for adjacent in self.adjacents:
            num_inner_adjacent_cubes += adjacent.num_adjacent_cubes
        return num_inner_adjacent_cubes

class OutbreakMarker():
    def __init__(self):
        self.position = 0
        self.limit = 8
        print("Setting outbreak marker...")

    def increase(self, game):
        self.position += 1
        if self.position == self.limit:
            game.end_game()
        # if self.position == self.limit:
            ### Game over

class InfectionRateMarker():
    def __init__(self):
        self.ir_hierarchy = [2, 2, 2, 3, 3, 4, 4]
        self.ir_index = 0
        self.infection_rate = self.ir_hierarchy[self.ir_index]
        print("Setting infection rate marker...")

    def increase(self):
        self.ir_index += 1
        self.infection_rate = self.ir_hierarchy[self.ir_index]

# class DiseaseCube():
#     def __init__(self, colour):
#         self.colour = colour

class Deck():
    def __init__(self, cards):
        self.cards = cards

    def shuffle(self):
        pass

class Card():
    def __init__(self):
        pass

    class PlayerCard():
        def __init__(self, city):
            self.city = city

    class EpidemicCard():
        pass

    class InfectionCard():
        def __init__(self, city):
            self.city = city

    class RoleCard():
        def __init__(self, role):
            self.role = role

def final_comma_ampersand(l):
    if isinstance(l, list):
        l = ", ".join(l)
        last_comma_index = l.rfind(",")
        if last_comma_index != -1:
            return l[:last_comma_index] + " &" + l[last_comma_index + 1:]
        else:
            return ""
    else:
        return l
