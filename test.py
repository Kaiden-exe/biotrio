from code.classes.protein import Protein
from code.classes.aminoacid import AminoAcid
from code.algorithms.proteinfolding import random_folding, fold_random, bonds
import csv
from code.algorithms.load_proteins import load_proteins
from code.algorithms.grid import create_grid
from code.visualisation.output import writecsv
from matplotlib import pyplot
import numpy as np


# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib as mpl

# m = [[ 0,0,0 ],
#     [0,1,0],
#     [0,0,0]]
    
# plt.figure()
# plt.matshow(m)
# plt.savefig("figure.png", format="png")


# grids = [[0] * 6 for _ in range(6)]

# i = 0
# for grid in grids:
#     print(grids[i])
#     i =+ 1

  # test_protein = Protein("data/testprotein.csv")

# protein_id = 2
# protein_order = "HHPPHP"

# eiwit = Protein(protein_id, protein_order)
# print(eiwit.aminoacids)

# print(random_folding())

source = "data/testprotein.csv"
proteins = load_proteins(source)
protein = proteins[0]
fold_random(protein)
protein.score = bonds(protein)
writecsv(protein, "test")
# grid = create_grid(len(protein.aminoacids))
# position = 0
# for acid in protein.aminoacids:
#     grid[0][position] = protein.aminoacids[position]
#     position += 1

# Initieren van de grid met correcte startpositie
# grid = create_grid(len(protein.aminoacids))
# startpos = len(protein.aminoacids)
# positionY = positionX = startpos
# grid[positionY][positionX] = protein.aminoacids[0]
# protein.aminoacids[0].folding = 1

# # Het eiwit afmaken aan de hand van folding
# for acid in protein.aminoacids[1:]:
#     while True:
#         folding = random_folding()
#         # Rotate amino acid over the X-axis
#         if folding == 1 or folding == -1:
#             positionXb = positionX + folding

#         # Rotate amino acid over the Y-axis
#         else:
#             positionYb = positionY + int(folding/2)
        
#         if grid[positionYb][positionXb] == 0:
#             positionX = positionXb
#             positionY = positionYb
#             grid[positionY][positionX] = acid
#             acid.folding = folding
#             break
#         else:
#             print("overschrijft")

# # Berekenen wat de stabiliteit is van de huidige vouwing.
# ## bonds(grid)

# print(grid)
# for row in grid:
#     print(row)