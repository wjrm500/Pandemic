import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title("Pandemic Outbreak Assistant")

from outbreak_sim import *

g = Game()

generic_width = 15

def click():
    g.outbroken_cities = []
    for city, value in input_dict.items():
        try:
            cubes_to_add = int(value["entry"].get())
            for i in range(0, cubes_to_add):
                g.cities[city].add_cube(g.cities[city].color, g)
        except:
            pass
    city_to_infect = submit_clicked.get()
    g.cities[city_to_infect].add_cube(g.cities[city_to_infect].color, g)

    for key, value in g.cities.items():
        if value.num_cubes > 0:
            output_dict[key]["entry"].delete(0, tk.END)
            output_dict[key]["entry"].insert(tk.END, str(value.num_cubes))

    for outbroken_city in g.outbroken_cities:
        output_dict[outbroken_city.name]["label"].config(relief = "solid", font = "Arial 9 bold", bg = "white", fg = "red")

def reset():
    submit_clicked.set("Select city...")
    for value in input_dict.values():
        value["entry"].delete(0, tk.END)
    for value in output_dict.values():
        value["label"].config(relief = "flat", font = "Arial 9", bg = value["bg_color"], fg = value["fg_color"])
        value["entry"].delete(0, tk.END)
    for city in g.cities.values():
        city.num_cubes = 0
    g.outbroken_cities = []
    # submit.focus_set()

def output_input():
    submit_clicked.set("Select city...")
    for value in input_dict.values():
        value["entry"].delete(0, tk.END)
    for city, value in output_dict.items():
        input_dict[city]["entry"].insert(tk.END, value["entry"].get())
    for value in output_dict.values():
        value["label"].config(relief = "flat", font = "Arial 9", bg = value["bg_color"], fg = value["fg_color"])
        value["entry"].delete(0, tk.END)
    g.outbroken_cities = []
    # submit.focus_set()

tk.Label(window, width = 7).grid(row = 0, column = 3)
tk.Label(window, width = 7).grid(row = 0, column = 5)
tk.Label(window, width = 7).grid(row = 0, column = 7)
tk.Label(window, width = 7).grid(row = 0, column = 9)

tk.Label(window, width = 2).grid(column = 0)
tk.Label(window, text = "City to infect", width = generic_width, anchor = "w").grid(row = 1, column = 1)
submit_clicked = tk.StringVar()
submit_clicked.set("Select city...")
options = [city for city in sorted(g.cities)]
submit = ttk.Combobox(window, textvariable = submit_clicked, values = options, state="readonly")
submit.config(width = generic_width)
submit.grid(row = 1, column = 2)

tk.Button(window, text = "Go!", command = click, width = 4).grid(row = 1, column = 3)
tk.Label(window).grid(row = 2)
tk.Label(window, text = "Cubes before", width = generic_width, anchor = "w").grid(row = 3, column = 1)
tk.Label(window).grid(row = 15)
tk.Label(window, text = "Cubes after", width = generic_width, anchor = "w").grid(row = 16, column = 1)
tk.Label(window).grid(row = 27)
tk.Button(window, text = "Reset", command = reset, width = 4).grid(row = 1, column = 7)
tk.Button(window, text = "Output -> Input", command = output_input, width = 12).grid(row = 1, column = 8)
tk.Button(window, text = "Exit", command = window.quit, width = 4).grid(row = 1, column = 9)
tk.Label(window, width = 2).grid(column = 10)

cities = {}
for color in ["Black", "Blue", "Red", "Yellow"]:
    color_cities = [city.name for city in g.cities.values() if city.color == color]
    cities[color] = sorted(color_cities)

### Input

input_dict = {}
for i, (color, color_cities) in enumerate(cities.items()):
    for j, city in enumerate(color_cities):
        font_color = "black" if color == "Yellow" else "white"
        input_label = tk.Label(window, text = city, bg = color, fg = font_color, width = generic_width, anchor = "w", font = "Arial 9")
        input_label.grid(row = j + 3, column = i * 2 + 2)
        input_entry = tk.Entry(window, width = 5)
        input_entry.grid(row = j + 3, column = i * 2 + 3)
        input_dict[city] = {"bg_color": color, "fg_color": font_color, "label": input_label, "entry": input_entry}

### Output

output_dict = {}
for i, (color, color_cities) in enumerate(cities.items()):
    for j, city in enumerate(color_cities):
        font_color = "black" if color == "Yellow" else "white"
        output_label = tk.Label(window, text = city, bg = color, fg = font_color, width = generic_width, anchor = "w", font = "Arial 9")
        output_label.grid(row = j + 16, column = i * 2 + 2)
        output_entry = tk.Entry(window, width = 5)
        output_entry.grid(row = j + 16, column = i * 2 + 3)
        output_dict[city] = {"bg_color": color, "fg_color": font_color, "label": output_label, "entry": output_entry}

window.mainloop()
