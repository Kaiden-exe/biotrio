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
from code.algorithms.greedy import Greedy
from code.algorithms.hill_climber import HillClimber
from code.visualisation.output import writecsv
from visualize import visualize, hist
from code.algorithms.simulated_annealing import Simulated_Annealing
from code.algorithms.depth_first import DepthFirst

if __name__ == "__main__":
    # Order: data/file, protein id
    if len(sys.argv) == 3:
        source = sys.argv[1]
        protein_id = sys.argv[2]

    protein = Protein(source, protein_id)

    while True:
        algor = input("Which algorithm do you want to run?\n r = random\n g = greedy\n h = hill climber\n s = simulated annealing\n d = depth first\n")
        if algor in ['r', 'g', 'h', 's', 'd']:
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
    elif algor == 'g':
        art = Greedy(protein)
        art.run_greedy(protein, runs)
    elif algor == 'd':
        art = DepthFirst(protein)
        art.run()
    elif algor == 'h':        
        while True:
            mutations = input("How many mutations do you want to make per run?\n")
            try:
                mutations = int(mutations)
                break
            except ValueError:
                print("Please give a positive integer.")

        art = HillClimber(protein)
        art.hike(runs, mutations)
    elif algor == 's':
        while True:
            temp = input("What initial temperature do you want?\n")
            try:
                temp = int(temp)
                break
            except ValueError:
                print("Please give a positive integer.")

        while True:
            mutations = input("How many mutations do you want to make per run?\n")
            try:
                mutations = int(mutations)
                break
            except ValueError:
                print("Please give a positive integer.")

        art = Simulated_Annealing(protein, temp)
        art.hike(runs, mutations)
        
    best = art.get_best()
    hist(art)
    writecsv(protein, best)
    visualize(best)

    print("Program completed!")