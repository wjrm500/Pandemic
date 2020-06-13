### This program makes the assumption that subpiles are as even as possible

import itertools
import numpy as np
import pandas as pd
import warnings

def ep_calculator(num_players, cards_in_hands, total_epidemics, epidemics_drawn, num_player_discards):
    total_player_cards = 53 + total_epidemics
    player_cards_drawn = num_player_discards + epidemics_drawn + np.sum([i for i in cards_in_hands.values()])
    player_cards_remaining = total_player_cards - player_cards_drawn

    removed_at_begin = 9 if num_players == 3 else 8
    pc = total_player_cards - removed_at_begin
    ec = total_epidemics
    a = int(np.floor(pc / ec))
    b = [a for i in range(6)]
    c = pc - np.sum(b)
    for i in range(c):
        b[i] += 1
    d = list(itertools.permutations(b))
    e = list(set(d))

    dicts_list = []
    for permutation in e:
        pc = total_player_cards - removed_at_begin
        dict = {}
        for index, value in enumerate(permutation):
            for j in range(value):
                subpile_num = index + 1
                epidemic_chance = (j + 1) / value
                dict[pc] = {"subpile_num": subpile_num, "epidemic_chance": epidemic_chance}
                pc -= 1
        dicts_list.append(dict)

    # print(dict)

    df = pd.DataFrame.from_dict(dicts_list)
    df = df.transpose()

    # print(df)

    dict = {}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category = RuntimeWarning)
        for index, row in df.iterrows():
            c = []
            for value in row:
                if value["subpile_num"] > epidemics_drawn + 1:
                    pass
                elif value["subpile_num"] > epidemics_drawn:
                    c.append(value["epidemic_chance"])
                elif value["subpile_num"] == epidemics_drawn:
                    c.append(0)
            dict[index] = np.mean(c)

    # print(dict)

    probability = dict[player_cards_remaining]
    return probability

num_players = int(input("How many players are playing?\n"))
if num_players not in [2, 3, 4]:
    raise ValueError("Invalid input")
print("")
cards_in_hands = {}
for i in range(num_players):
    cards_in_hands[i] = int(input("How many cards does player {} have in their hand?\n".format(i + 1)))
    print("")
total_epidemics = int(input("How many epidemic cards did you begin with?\n"))
print("")
epidemics_drawn = int(input("And how many epidemic cards have you drawn?\n"))
print("")
num_player_discards = int(input("Finally, how many cards are in the player discard pile?\n"))
print("")

### First card draw
a = ep_calculator(num_players, cards_in_hands, total_epidemics, epidemics_drawn, num_player_discards)

### If epidemic drawn
epidemics_drawn += 1
b = ep_calculator(num_players, cards_in_hands, total_epidemics, epidemics_drawn, num_player_discards)

### If other player card drawn
epidemics_drawn -= 1
cards_in_hands[0] += 1
c = ep_calculator(num_players, cards_in_hands, total_epidemics, epidemics_drawn, num_player_discards)

def zin(num): ### Zero if nan
    if np.isnan(num):
        return 0
    else:
        return num

nil_nil = zin(1 - a) * zin(1 - c) ### 0 epidemic cards drawn
one_nil = zin(a) * zin(1 - b) ### Epidemic card drawn on first draw; no epidemic card drawn on second draw
nil_one = zin(1 - a) * zin(c) ### No epidemic card drawn on first draw; epidemic card drawn on second draw
one_one = zin(a) * zin(b) ### 2 epidemic cards drawn

at_least_one = one_nil + nil_one + one_one

import time, sys
for i in range(4):
    sys.stdout.write("\r" + "Calculating" + "." * i)
    time.sleep(0.5)
    sys.stdout.flush()
print("")
if not np.isnan(a):
    one_nil = np.around(one_nil * 100, decimals = 2)
    at_least_one = np.around(at_least_one * 100, decimals = 2)
    one_one = np.around(one_one * 100, decimals = 2)
    print("The chance of the next player card being an epidemic is {}%".format(one_nil))
    time.sleep(0.5)
    print("The chance of at least one of the next two player cards being an epidemic is {}%".format(at_least_one))
    time.sleep(0.5)
    print("The chance of both of the next two player cards being epidemics is {}%".format(one_one))
else:
    print("You must have made a mistake!")
