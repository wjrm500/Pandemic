import pandas as pd

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
                pass
            for adjacent in self.adjacents:
                adjacent.num_adjacent_cubes += 1
        else:
            if self in game.outbroken_cities:
                pass
            else:
                self.outbreak(game)

    def outbreak(self, game):
        game.outbroken_cities.append(self)
        adjacent_city_names = []
        for adjacent in self.adjacents:
            adjacent_city_names.append(adjacent.name)
        adjacent_city_names = final_comma_ampersand(adjacent_city_names)
        game.outbreak_marker.increase(game)
        for adjacent in self.adjacents:
            adjacent.add_cube(self.colour, game)
            cube_cubes = "cube" if adjacent.num_cubes == 1 else "cubes"

class Game():
    def __init__(self):
        self.outbreak_marker = OutbreakMarker()
        self.outbroken_cities = []

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

        ### Populating cities' adjacent cities lists with city objects

        for city in self.cities.values():
            adjacents = city.adjacents
            adjacent_objects = []
            for adjacent in adjacents:
                adjacent_objects.append(self.cities.get(adjacent))
            city.adjacents = adjacent_objects

class OutbreakMarker():
    def __init__(self):
        self.position = 0
        self.limit = 8

    def increase(self, game):
        self.position += 1

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
