from .random import Random
from code.classes.protein import Protein
from code.classes.aminoacid import AminoAcid
import random
import copy

class Greedy(Random):
    """
    A Greedy algorithm that builds a stack of proteins with a unique folding for each instance.
    """
    def __init__(self, protein):
        super().__init__()
        self.protein = protein
        # List of all [Score, Folding] combinations
        self.best = []
        # List that keeps track of foldings per amino acid
        self.prev_fold = 0
        self.positionX = 0
        self.positionY = 0
        self.i = 0


    def fold(self):
        '''
        Returns a specific folding value.
        '''
        folding = self.get_best_fold(self.protein)

        if folding == None:
            self.prev_fold = 0
        else:
            self.prev_fold = folding

        return folding


    def get_best_fold(self, protein):
        '''
        Find the best folding for the next amino acid.
        '''
        self.best = []

        # Acquire list of all foldings to try
        fold_list = Protein.get_fold_list(protein)

        if not self.prev_fold == 0:
            fold_list.remove(-self.prev_fold)

        # Remove folds from list if in forbidden lists
        acid = protein.aminoacids[self.i]
        for j in range(len(acid.forbidden_folds)):
            if acid.forbidden_folds[j] in fold_list:
                fold_list.remove(acid.forbidden_folds[j])

        # Try all possible foldings and return a random one of the best options
        for k in range(len(fold_list)):
            folding = fold_list[k]
            temp_fold = self.get_temp_coordinates(folding)
            trial = self.try_fold(protein, temp_fold)

            if trial == True:
                self.add_best(protein, temp_fold)
            else:
                pass
        
        if self.best:
            random_best = random.choice(self.best)
        else:
            return None

        new_fold = self.get_temp_coordinates(random_best[1])
        self.positionX = new_fold[0]
        self.positionY = new_fold[1]

        return random_best[1]

    
    def try_fold(self, protein, temp_fold):
        '''
        Make a temporary fold of an aminoacid and return temporary stability score or None if the fold is N.A.
        '''
        positionXb = temp_fold[0]
        positionYb = temp_fold[1]

        # Assume position if X and Y coordinates are not already occupied by a previous amino acid
        if not (positionXb, positionYb) in protein.positions.keys():
            return True
        else:
            return False


    def get_temp_coordinates(self, folding):
        '''
        Returns the coordinates for the next amino according to the temporary folding of the previous amino.
        '''
        # Rotate amino acid over the X-axis
        if folding == 1 or folding == -1:
            yb = self.positionY
            xb = self.positionX + folding

        # Rotate amino acid over the Y-axis
        else:
            xb = self.positionX
            yb = self.positionY + int(folding/2)
        
        return [xb, yb, folding]

    
    def add_best(self, protein, temp_fold):
        # TODO - docstring looks incomplete
        '''
        Adds stability folding for next aminoacid to temporary list self.best, if best
        '''
        positionXb = temp_fold[0]
        positionYb = temp_fold[1]
        folding = temp_fold[2]

        temp_protein = copy.deepcopy(protein)

        temp_protein.add_position(protein.aminoacids[self.i+1], positionXb, positionYb)
        temp_protein.set_stability()
        
        temp_score = temp_protein.score

        del temp_protein

        # Check if this folding gains a higher stability than previous tries
        if self.best:
            if temp_score < self.best[0][0]:
                self.best.clear()
                self.best.append([temp_score, folding])
            else:
                for j in range(len(self.best)):
                    if temp_score == self.best[j][0]:
                        self.best.append([temp_score, folding])
                        break
        else:
            self.best.append([temp_score, folding])


    def run_greedy(self, protein, runs):
        '''
        Fold the protein according to the greedy algorithm x times.
        '''
        for k in range(runs):
            
            # Keep track of progression while running
            if k % 1000 == 0:
                print(f"Total number of iterations done: {k}")

            # Finish a protein with greedy folding
            self.positionX = self.positionY = 0
            self.i = 0

            # Loop through a protein and fill in each amino acid per iteration
            while self.i < len(protein.aminoacids):
                protein.add_position(protein.aminoacids[self.i], self.positionX, self.positionY)
                self.i, self.positionX, self.positionY = self.fold_random(protein, self.positionX, self.positionY, self.i)
                
                # Reset the protein if no folds are able for the next amino acid
                if self.i == 0:
                    protein.positions.clear()

            protein.set_stability()
            self.add_solution(protein)


class GreedyLookahead(Greedy):
    """
    The greedy lookahead algorithm will configure an X amount of amino acids at once
    to calculate a corresponding stability score.
    The first amino acid will be placed according to the best stability score found,
    from where the same pattern will be repeated.
    """
    def __init__(self, protein, lookahead):
        super().__init__(protein)
        self.lookahead = lookahead

    def run_greedy(self, protein, runs):
        '''
        Fold the protein according to the greedy lookahead algorithm.
        '''
        for k in range(runs):
            
            # Keep track of progression while running
            if k % 1000 == 0:
                print(f"Total number of iterations done: {k}")

            # Finish a protein with greedy folding
            self.positionX = self.positionY = 0
            self.i = 0

            # Loop through a protein and fill in each amino acid per iteration
            while self.i < len(protein.aminoacids):
                protein.add_position(protein.aminoacids[self.i], self.positionX, self.positionY)
                self.i, self.positionX, self.positionY = self.fold_random(protein, self.positionX, self.positionY, self.i)
                
                # Reset the protein if no folds are able for the next amino acid
                if self.i == 0:
                    protein.positions.clear()

            protein.set_stability()
            self.add_solution(protein)


    def get_best_fold(self, protein):
        '''
        Find the best folding for the next amino acid according to X amount of amino acids placed in the upcoming acids.
        '''
        self.best = []

        # Acquire list of all foldings to try
        fold_list = Protein.get_fold_list(protein)

        if not self.prev_fold == 0:
            fold_list.remove(-self.prev_fold)

        # Remove folds from list if in forbidden lists
        acid = protein.aminoacids[self.i]
        for j in range(len(acid.forbidden_folds)):
            if acid.forbidden_folds[j] in fold_list:
                fold_list.remove(acid.forbidden_folds[j])

        # Try all possible foldings and return a random one of the best options
        for k in range(len(fold_list)):
            folding = fold_list[k]
            temp_fold = self.get_temp_coordinates(folding)
            trial = self.try_fold(protein, temp_fold)

            if trial == True:
                self.add_best(protein, temp_fold)
            else:
                pass
        
        if self.best:
            random_best = random.choice(self.best)
        else:
            return None

        new_fold = self.get_temp_coordinates(random_best[1])
        self.positionX = new_fold[0]
        self.positionY = new_fold[1]

        return random_best[1]
