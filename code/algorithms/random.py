from code.classes.aminoacid import AminoAcid
from code.classes.protein import Protein
import random
import copy

class Random():
    def __init__(self):
        self.solutions = []
        self.protein = None

    
    def fold(self):
        '''
        Folds a protein randomly. # chooses a random direction for the folding
        '''
        fold_list = Protein.get_fold_list(self.protein)
        folding = random.choice(fold_list)
        return folding


    def fold_random(self, protein, positionX, positionY, i):
        '''
        Folds the next amino acid randomly.
        '''
        loop = []
        acid = protein.aminoacids[i]

        while True:
            if acid == protein.aminoacids[-1]:
                acid.folding = 0
                i += 1
                
                return i, positionX, positionY
            
            new_coordinates = self.get_new_coordinates(positionX, positionY)
            
            # Fail save for greedy algorithm
            if new_coordinates == [None, None, None]:
                return 0, 0, 0
            
            positionXb = new_coordinates[0]
            positionYb = new_coordinates[1]
            folding = new_coordinates[2]
            
            # Assume position if X and Y coordinates are not already occupied by a previous acid
            if not (positionXb, positionYb) in protein.positions.keys() and not folding in acid.forbidden_folds:
                positionX = positionXb
                positionY = positionYb
                acid.folding = folding
                i += 1

                return i, positionX, positionY
            else:
                if not folding in loop:
                    loop.append(folding)

            if len(loop) == len(Protein.get_fold_list(self.protein)):
                i -= 1
                new_coordinates = protein.remove_last()
                positionX = new_coordinates[0]
                positionY = new_coordinates[1]
                
                return i, positionX, positionY
                
    
    def run_random(self, protein, x):
        '''
        Fold the protein randomly x times.
        '''
        self.protein = protein

        for _ in range(x):

            # Finish a protein with random folding 
            positionX = positionY = 0
            i = 0
    
            while i < len(protein.aminoacids):
                protein.add_position(protein.aminoacids[i], positionX, positionY)
                i, positionX, positionY = self.fold_random(protein, positionX, positionY, i)

            protein.set_stability()
            self.add_solution(protein)

        
    
    def add_solution(self, protein):
        '''
        Add a solution to the list of solutions.
        '''
        score = protein.score
        copy_dict = copy.deepcopy(protein.positions)
        self.solutions.append([score, copy_dict])
        protein.clear_protein()


    def get_best(self):
        '''
        Returns the best solution from all generated solutions.
        '''
        best = [1]
        for lst in self.solutions:
            if lst[0] < best[0]:
                best = lst

        return best


    def get_new_coordinates(self, x, y):
        '''
        Returns the coordinates for the next aminoacid according to the folding of the previous amino acid.
        '''
        # Chooses a random fold over the x-axis (-1, 1) or the y-axis (-2, 2).
        folding = self.fold()

        # Fail save for greedy algorithm
        if folding == None:
            return [None, None, None]
        
        # Rotate amino acid over the X-axis
        if folding == 1 or folding == -1:
            yb = y
            xb = x + folding

        # Rotate amino acid over the Y-axis
        else:
            xb = x
            yb = y + int(folding/2)
        
        return [xb, yb, folding]