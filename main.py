from game import Game
from objects import Card


p = [
    "Iain",
    "Will",
    # "Ruben",
    # "Will",
]
g = Game(players = p, difficulty = "Introductory")

# for player in g.players:
#     print(player.role.name)
g.go()

# for city in sorted(g.cities.values(), key = lambda x: x.colour):
#     print(city.name, city.num_cubes)



# for city in g.cities.values():
#     if city.num_cubes > 0:
#         cube_cubes = "cube" if city.num_cubes == 1 else "cubes"
#         print("{} - {} {}".format(city.name, city.num_cubes, cube_cubes))
