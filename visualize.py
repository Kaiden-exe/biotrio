import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from code.classes.protein import Protein
from code.algorithms.grid import create_grid
from code.algorithms.load_proteins import load_proteins
from code.algorithms.proteinfolding import fold_random

def visualize():
    # Retreive data folded protein
    source = "data/testprotein.csv"
    proteins = load_proteins(source)

    # Retreive length to create grid
    curr_protein = proteins[0]
    protein_length = len(curr_protein.aminoacids)

    fold_random(curr_protein)

    protein_dict = curr_protein.positions
    protein = curr_protein.positions
    print(protein_dict)

    # Render empty grid
    grid = create_grid(protein_length)

    # Fill the grid with all the amino acids
    for x, y in protein.keys():
        acid = protein[(x, y)]
        grid[x][y] = acid.id

    # Turn different amino acids in corresponding colors
    # Empty(0): Purple, H(1): Green, P(2): Yellow
    # lstcount = 0
    # for lst in grid:
    #     numbercount = 0
    #     for number in lst:
    #         if grid[lstcount][numbercount] == 'H':
    #             grid[lstcount][numbercount] = 1
    #         elif grid[lstcount][numbercount] == 'P':
    #             grid[lstcount][numbercount] = 2
    #         numbercount += 1
    #     lstcount += 1

    lstcount = 0
    for lst in grid:
        numbercount = 0
        for number in lst:
            if number == 'H':
                grid[lstcount][numbercount] = 1
            elif number == 'P':
                grid[lstcount][numbercount] = 2
            numbercount += 1
        lstcount += 1

    # Plot figure of the grid
    print(grid)
    plt.figure()
    plt.matshow(grid)
    plt.savefig("grid.png", format="png")

    # As rendering voor wanneer negatieve waardes wel geprint kunnen worden.
    # plt.xlim(-5.5)
    # plt.ylim(-5,5)