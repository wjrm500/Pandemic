import itertools
import numpy as np
import pandas as pd

num_players = int(input("How many players are playing?\n"))
dict = {}
for i in range(num_players):
    dict[i] = int(input("How many cards does player {} have in their hand?\n".format(i + 1)))
total_epidemics = int(input("How many epidemic cards did you begin with?\n"))
epidemics_drawn = int(input("And how many have you drawn?\n"))
num_player_discards = int(input("Finally, how many cards are in the player discard pile?\n"))

total_player_cards = 53 + total_epidemics
player_cards_drawn = num_player_discards + epidemics_drawn + np.sum([i for i in dict.values()])
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
    pc = player_cards_remaining
    dict = {}
    for index, value in enumerate(permutation):
        for j in range(value):
            subpile_num = index + 1
            epidemic_chance = (j + 1) / value
            dict[pc] = {"subpile_num": subpile_num, "epidemic_chance": epidemic_chance}
            pc -= 1
    dicts_list.append(dict)

df = pd.DataFrame.from_dict(dicts_list)
df = df.transpose()

dict = {}
for index, row in df.iterrows():
    c = []
    for value in row:
        if value["subpile_num"] > epidemics_drawn:
            c.append(value["epidemic_chance"])
        elif value["subpile_num"] == epidemics_drawn:
            c.append(0)
    dict[index] = np.mean(c)

print("The chances of the next player card being an epidemic are {}".format(dict[player_cards_remaining]))
