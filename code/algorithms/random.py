from code.classes.aminoacid import AminoAcid
from code.classes.protein import Protein
import random
import copy

class Random():
    def __init__(self):
        self.solutions = []

    
    def fold(self):
        '''
        Folds a protein randomly. # chooses a random direction for the folding
        '''
        fold_list = [-1, 1, -2, 2]
        x = random.choice(fold_list)
        return x


    def fold_random(self, protein):
        '''
        Folds a protein randomly. 
        '''
        
        positionX = positionY = positionXb = positionYb = 0

        # print(protein.aminoacids)
        
        # Finish the protein with random folding 
        i = 0
        while i < len(protein.aminoacids):
            acid = protein.aminoacids[i]
            protein.add_position(acid, positionX, positionY)
            loop = 0
            while True:
                if acid == protein.aminoacids[-1]:
                    acid.folding = 0
                    break
                
                # chooses a random fold over the x-axis (-1, 1) or the y-axis (-2, 2).
                folding = self.fold()
                
                # Rotate amino acid over the X-axis
                if folding == 1 or folding == -1:
                    positionYb = positionY
                    positionXb = positionX + folding

                # Rotate amino acid over the Y-axis
                else:
                    positionXb = positionX
                    positionYb = positionY + int(folding/2)
                
                # Assume position if X and Y coordinates are not already occupied by a previous acid
                if not (positionXb, positionYb) in protein.positions.keys():
                    positionX = positionXb
                    positionY = positionYb
                    acid.folding = folding
                    break
                else:
                    loop += 1

                if loop == 3:
                    i -= 1
                    # TODO: write method to remove the acid with the highest index from protein.positions
                    protein.remove_last()
                    break
                

    
    def run_random(self, protein, x):
        '''
        Fold the protein randomly x times.
        '''
        for _ in range(x):
            self.fold_random(protein)
            protein.set_stability()
            self.add_solution(protein)

        
    
    def add_solution(self, protein):
        copy_score = copy.deepcopy(protein.score)
        copy_dict = copy.deepcopy(protein.positions)
        self.solutions.append([copy_score, copy_dict])
        protein.score = 0
        protein.positions.clear()


    def get_best(self):
        best = [1]
        for lst in self.solutions:
            if lst[0] < best[0]:
                best = lst
        return best


        # # if the solutions list is empty, add scores
        # if len(protein.solutions) == 0:
        #     protein.solutions.append([protein.score, protein.positions])

        # item = protein.solutions[0]:
        # if item[0] < protein.score:
        #     protein.solutions.clear()
        #     protein.solutions.append([protein.score, protein.positions])


        # len(list)/x = % of best solutions