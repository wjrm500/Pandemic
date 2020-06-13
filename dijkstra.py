import pandas as pd
import numpy as np
import networkx as nx

g = nx.Graph()
df = pd.read_csv("pandemic_cities.csv")

for index, row in df.iterrows():
    for adjacent in row[2:]:
        if pd.notnull(adjacent):
            g.add_edge(row["City"], adjacent)

num_cities = len(df["City"])
average_path_lengths = {}
for source_city in df["City"]:
    path_length_sum = 0
    for target_city in df["City"]:
        path_length_sum += nx.dijkstra_path_length(g, source_city, target_city)
    average_path_length = path_length_sum / num_cities
    average_path_lengths[source_city] = average_path_length

path_df = pd.DataFrame.from_dict(average_path_lengths.items())
path_df.rename(columns = {0: "City", 1: "Avg_Path_Length"}, inplace = True)
print(path_df.sort_values(by = "Avg_Path_Length"))
