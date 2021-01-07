from code.classes.protein import Protein
from code.classes.aminoacid import AminoAcid
from code.algorithms.proteinfolding import random_folding
import csv
from code.algorithms.load_proteins import load_proteins
from code.algorithms.grid import create_grid
from matplotlib import pyplot
import numpy as np

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
print(proteins)
protein = proteins[0]
# grid = create_grid(len(protein.aminoacids))
# position = 0
# for acid in protein.aminoacids:
#     grid[0][position] = protein.aminoacids[position]
#     position += 1

grid = create_grid(len(protein.aminoacids))

print(grid)
pyplot.matshow(grid)
pyplot.show()
print("piemel")

startpos = len(protein.aminoacids)
positionY = positionX = startpos
grid[positionY][positionX] = protein.aminoacids[0]
protein.aminoacids[0].folding = 1

# Het eiwit afmaken aan de hand van folding
for acid in protein.aminoacids[1:]:
    while True:
        folding = random_folding()
        # Rotate amino acid over the X-axis
        if folding == 1 or folding == -1:
            positionX += folding

        # Rotate amino acid over the Y-axis
        else:
            positionY += int(folding/2)
        

        # HIER MOET EVEN GEFIXT WORDEN DAT BIJ ELKE OVERSCHRIJVING DE COORDINATEN GERESET WORDEN !!!!!!!!!!!!
        if grid[positionY][positionX] == 0:
            grid[positionY][positionX] = acid
            acid.folding = folding
            break
        else:
            print("overschrijft")

print(grid)
for row in grid:
    print(row)


# pyplot.imshow(grid)
# pyplot.show()