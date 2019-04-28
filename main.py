import pandas as pd
import networkx as nx
import datetime
from heapq import nsmallest
import math
from pyvis.network import Network


def create_date(row):
    return datetime.date(row['iyear'], row['imonth'], row['iday'])


def distance(row1, row2):
    date1 = create_date(row1)
    date2 = create_date(row2)
    delta_days = math.pow((date2 - date1).days, 2)
    delta_kills = math.pow(row2['nkill'] - row1['nkill'], 2)
    return math.sqrt(delta_days + delta_kills)


data = pd.read_csv("data.csv", encoding="ISO-8859-1")
dates_and_kills = data[['iyear', 'imonth', 'iday', 'nkill', 'city', 'country_txt']].dropna()
dates_and_kills = dates_and_kills.loc[
    (dates_and_kills['iyear'] >= 2017) & (dates_and_kills['nkill'] > 0) & (dates_and_kills['imonth'] > 0) & (
            dates_and_kills['iday'] > 0)].head(1000)
G = nx.Graph()
labels = {}
for index, row in dates_and_kills.iterrows():
    distances = {}
    G.add_node(index, title=row['city'])
    for index2, row2 in dates_and_kills.iterrows():
        if not G.has_edge(index, index2):
            if index != index2:
                distances[index2] = distance(row, row2)
    smallest = nsmallest(3, distances, key=distances.get)
    for neighbour in smallest:
        G.add_edge(index, neighbour)
    labels[index] = row['city'] + ", " + row['country_txt'] + ' on ' + create_date(row).strftime("%d %b, %Y")
g = Network(height=1200, width=1200, notebook=True, bgcolor="#222222", font_color="white")
g.toggle_hide_edges_on_drag(False)
g.from_nx(G)

for node in g.nodes:
    node["title"] = labels[node["id"]]

g.show("ex.html")
nx.write_edgelist(G, "graph.txt")
