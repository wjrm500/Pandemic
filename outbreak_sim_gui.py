import tkinter as tk

window = tk.Tk()
window.title("Pandemic Outbreak Assistant")

generic_width = 15

def click():
    for city, entry in input_entry_dict.items():
        try:
            cubes_to_add = int(entry.get())
            for i in range(0, cubes_to_add):
                g.cities[city].add_cube(g.cities[city].colour, g)
        except:
            pass
    city_to_infect = submit.get()
    g.cities[city_to_infect].add_cube(g.cities[city_to_infect].colour, g)

    for key, value in g.cities.items():
        if value.num_cubes > 0:
            output_entry_dict[key].delete(0, tk.END)
            output_entry_dict[key].insert(tk.END, str(value.num_cubes))

def reset():
    submit.delete(0, tk.END)
    for entry in input_entry_dict.values():
        entry.delete(0, tk.END)
    for entry in output_entry_dict.values():
        entry.delete(0, tk.END)
    for city in g.cities.values():
        city.num_cubes = 0
    submit.focus_set()

tk.Label(window, width = 7).grid(row = 0, column = 3)
tk.Label(window, width = 7).grid(row = 0, column = 5)
tk.Label(window, width = 7).grid(row = 0, column = 7)
tk.Label(window, width = 7).grid(row = 0, column = 9)

tk.Label(window, width = 2).grid(column = 0)
tk.Label(window, text = "City to infect", width = generic_width, anchor = "w").grid(row = 1, column = 1)
submit = tk.Entry(window, width = generic_width + 3)
submit.grid(row = 1, column = 2)
tk.Button(window, text = "Go!", command = click, width = 4).grid(row = 1, column = 3)
tk.Label(window).grid(row = 2)
tk.Label(window, text = "Cubes before", width = generic_width, anchor = "w").grid(row = 3, column = 1)
tk.Label(window).grid(row = 15)
tk.Label(window, text = "Cubes after", width = generic_width, anchor = "w").grid(row = 16, column = 1)
tk.Label(window).grid(row = 27)
tk.Button(window, text = "Reset", command = reset, width = 4).grid(row = 1, column = 7)
tk.Button(window, text = "Exit", command = window.quit, width = 4).grid(row = 1, column = 9)
tk.Label(window, width = 2).grid(column = 10)

from outbreak_sim import *

g = Game()
cities = {}
for colour in ["Black", "Blue", "Red", "Yellow"]:
    colour_cities = [city.name for city in g.cities.values() if city.colour == colour]
    cities[colour] = sorted(colour_cities)

### Input

input_entry_dict = {}
for i, (colour, colour_cities) in enumerate(cities.items()):
    for j, city in enumerate(colour_cities):
        font_color = "black" if colour == "Yellow" else "white"
        tk.Label(window, text = city, bg = colour, fg = font_color, width = generic_width, anchor = "w").grid(row = j + 3, column = i * 2 + 2)
        input_entry = tk.Entry(window, width = 5)
        input_entry.grid(row = j + 3, column = i * 2 + 3)
        input_entry_dict[city] = input_entry

### Output

output_entry_dict = {}
for i, (colour, colour_cities) in enumerate(cities.items()):
    for j, city in enumerate(colour_cities):
        font_color = "black" if colour == "Yellow" else "white"
        tk.Label(window, text = city, bg = colour, fg = font_color, width = generic_width, anchor = "w").grid(row = j + 16, column = i * 2 + 2)
        output_entry = tk.Entry(window, width = 5)
        output_entry.grid(row = j + 16, column = i * 2 + 3)
        output_entry_dict[city] = output_entry



window.mainloop()
