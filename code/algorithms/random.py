from code.classes.aminoacid import AminoAcid
from code.classes.protein import Protein
import random

class Random():
    def fold_random(self, protein):
        '''
        Folds a protein randomly.
        '''
        positionX = positionY = positionXb = positionYb = 0
        protein.add_position(protein.aminoacids[0], positionX, positionY)
        protein.aminoacids[0].folding = 1

        # Finish the protein with random folding 
        for acid in protein.aminoacids[1:]:

            while True:
                # chooses a random fold over the x-axis (-1, 1) or the y-axis (-2, 2).
                fold_list = [-1, 1, -2, 2]
                folding = random.choice(fold_list) # this is what we will want to put in a separate function 
                
                # Rotate amino acid over the X-axis
                if folding == 1 or folding == -1:
                    positionXb = positionX + folding

                # Rotate amino acid over the Y-axis
                else:
                    positionYb = positionY + int(folding/2)
                
                # Assume position if X and Y coordinates are not already occupied by a previous acid
                if not (positionXb, positionYb) in protein.positions.keys():
                    positionX = positionXb
                    positionY = positionYb
                    protein.add_position(acid, positionX, positionY)
                    acid.folding = folding
                    break


    
    def run_random(self, protein, x):
        '''
        Fold the protein randomly x times.
        '''
        for _ in range(x):
            self.fold_random(protein)
            protein.set_stability()
            protein.add_solution()
            


        # # if the solutions list is empty, add scores
        # if len(protein.solutions) == 0:
        #     protein.solutions.append([protein.score, protein.positions])

        # item = protein.solutions[0]:
        # if item[0] < protein.score:
        #     protein.solutions.clear()
        #     protein.solutions.append([protein.score, protein.positions])


        # len(list)/x = % of best solutions