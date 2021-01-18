##################################################
## The Contortionist
##################################################
## This program calculates the optimal folding configuration for a protein.
##################################################
## Authors: Eva van der Heide, Kaiden Sewradj and Wouter Vincken
## License: unilicense 
## Version: 1.0.0
## Status: Unfinished
##################################################

# from code.classes.aminoacid import AminoAcid
# from code.classes.protein import Protein
# from code.algorithms import randomchoice

import sys
from code.classes.protein import Protein
from code.algorithms.random import Random
from code.visualisation.output import writecsv
from visualize import visualize, hist

if __name__ == "__main__":
    # Order: data/file, protein id
    if len(sys.argv) == 3:
        source = sys.argv[1]
        protein_id = sys.argv[2]

    protein = Protein(source, protein_id)

    while True:
        algor = input("Which algorithm do you want to run?\n r = random\n")
        if algor in ['r']:
            break
        else:
            print("Please select a valid algorithm.")
    
    while True:
        runs = input("How often do you want to run this algorithm?\n")
        try:
            runs = int(runs)
            break
        except ValueError:
            print("Please give a positive integer.")
    
    if algor == 'r':
        art = Random()
        art.run_random(protein, runs)
        best = art.get_best()

    hist(art)
    writecsv(protein, best)
    visualize(best)