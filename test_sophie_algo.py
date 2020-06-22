#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 21:40:09 2020

@author: sophierossi
"""
from graphe import *

g = Garage (2.2728354, 48.8281142997349, 40, 60)
c = Camion(50, 0, 10000)

k = 10 # choose number of clients
df, indexes, warehouses, parcels = create_graph_components(k)

G = Graph(g, warehouses, parcels, c)
G.make_graph()
G.generate_csv(df, indexes)

