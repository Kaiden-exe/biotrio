from code.classes.aminoacid import AminoAcid
from code.classes.protein import Protein
import random
import copy

class Random():
    '''
    Algorithm that folds the amino acids in the protein at random.
    '''
    def __init__(self):
        self.protein = None
        self.best = [0, {}]
        self.sol_dict = {}

    
    def fold(self):
        '''
        Chooses a random direction for the folding.
        '''
        fold_list = self.protein.get_fold_list()
        folding = random.choice(fold_list)
        
        return folding


    def fold_random(self, protein, positionX, positionY, i):
        '''
        Folds the next amino acid randomly.
        '''
        # Create list of unavailable folds to prevent infinite loops
        loop = []
        acid = protein.aminoacids[i]

        while True:
            if acid == protein.aminoacids[-1]:
                acid.folding = 0
                i += 1
                
                return i, positionX, positionY
            
            new_coordinates = self.get_new_coordinates(positionX, positionY)
            
            # Fail save for Greedy algorithm
            if new_coordinates == [None]:

                return 0, 0, 0
                
            # Fail save for GreedyLookahead algorithm
            elif type(new_coordinates) is dict:
                protein.aminoacids[-1].folding = 0

                return new_coordinates, 0, 0
            
            positionXb = new_coordinates[0]
            positionYb = new_coordinates[1]
            folding = new_coordinates[2]
            
            # Check if folding is valid
            if not (positionXb, positionYb) in protein.positions.keys() and not folding in acid.forbidden_folds:
                positionX = positionXb
                positionY = positionYb
                acid.folding = folding
                i += 1

                return i, positionX, positionY
            
            # Save fold in list of unavailable folds
            elif not folding in loop:
                loop.append(folding)

            # If every folding is invalid, change folding of the previous amino acid
            if len(loop) == len(self.protein.get_fold_list()):
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
            positionX = positionY = 0
            i = 0

            # Fold protein per amino acid
            while i < len(protein.aminoacids):
                protein.add_position(protein.aminoacids[i], positionX, positionY)
                i, positionX, positionY = self.fold_random(protein, positionX, positionY, i)

            protein.set_stability()
            self.add_solution(protein)

    
    def add_solution(self, protein):
        '''
        Add a solution to the list of solutions, and checks if it is best solution found yet.
        '''
        # Replace best folded protein if stability score is higher
        if protein.score < self.best[0]:
            self.best.clear()
            dic = copy.deepcopy(protein.positions)
            self.best = [protein.score, dic]
        elif self.best == [0, {}]:
            dic = copy.deepcopy(protein.positions)
            self.best = [protein.score, dic]

        # Count all found stability scores
        if protein.score in self.sol_dict.keys():
            self.sol_dict[protein.score] += 1
        else:
            self.sol_dict[protein.score] = 1

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
        # Get random folding
        folding = self.fold()

        # Fail save for greedy algorithm
        if folding == None:

            return [None]

        # Fail save for GreedyLookahead algorithm
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