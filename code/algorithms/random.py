from code.classes.aminoacid import AminoAcid
from code.classes.protein import Protein
import random
import copy

class Random():
    '''
    Algorithm that folds the amino acids in the protein at random.
    '''
    def __init__(self):
        self.solutions = []
        self.best = [0, {}]
        self.protein = None

    
    def fold(self):
        '''
        Chooses a random direction for the folding.
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
            
            # TODO - maybe explain in more detail what the comment below means
            # Fail save for greedy algorithm
            if new_coordinates == [None]:
                return 0, 0, 0
            # Fail save for GreedyLookahead algorithm
            elif type(new_coordinates) is dict:
                return new_coordinates, 0, 0
            
            positionXb = new_coordinates[0]
            positionYb = new_coordinates[1]
            folding = new_coordinates[2]
            
            # Assume position if X and Y coordinates are not already occupied by a previous amino acid
            if not (positionXb, positionYb) in protein.positions.keys() and not folding in acid.forbidden_folds:
                positionX = positionXb
                positionY = positionYb
                acid.folding = folding
                i += 1

                return i, positionX, positionY
            else:
                if not folding in loop:
                    loop.append(folding)

            # TODO - add a comment here
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

            # TODO - reword comment below: 'finish a protein'
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
        Add a solution to the list of solutions, and checks if it is best solution found yet.
        '''
        score = protein.score

        # Add to best if score is better than current best found
        if score < self.best[0]:
            self.best.clear()
            copy_dict = copy.deepcopy(protein.positions)
            
            self.best = [score, copy_dict]
            del copy_dict
        elif self.best == [0, {}]:
            copy_dict = copy.deepcopy(protein.positions)
            self.best = [score, copy_dict]
            del copy_dict

        self.solutions.append(score)
        protein.clear_protein()


    def get_best(self):
        '''
        Returns the best solution from all generated solutions.
        '''
        return self.best


    def get_new_coordinates(self, x, y):
        '''
        Returns the coordinates for the next amino acid according to the folding of the previous amino acid.
        '''
        # Chooses a random fold over the x-axis (-1, 1) or the y-axis (-2, 2)
        folding = self.fold()

        # TODO - explain comment below
        # Fail save for greedy algorithm
        if folding == None:
            return [None]
        elif type(folding) is dict:
            return folding
        
        # Rotate amino acid over the X-axis
        if folding == 1 or folding == -1:
            yb = y
            xb = x + folding

        # Rotate amino acid over the Y-axis
        else:
            xb = x
            yb = y + int(folding/2)
        
        return [xb, yb, folding]