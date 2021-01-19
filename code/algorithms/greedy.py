from .random import Random
from code.classes.protein import Protein
from code.classes.aminoacid import AminoAcid
import random
import copy

class Greedy(Random):
    def __init__(self):
        self.protein = Protein
        # List of all [Score, Folding] combinations
        self.best = []
        # List that keeps track of foldings per amino acid
        self.prev_fold = []
        self.positionX = 0
        self.positionY = 0
        self.i = 0


    def fold(self):
        '''
        Returns a specific folding value.
        '''
        folding = self.get_best_fold(self.protein)
        self.prev_fold = [folding]

        return folding


    # def fold_greedy(self, protein, positionX, positionY, i):
    #     '''
    #     1. alle opties fold van volgende aminozuur proberen
    #         2. van elke optie stability score berekenen
    #     3. fold returnen van optie met beste stability
    #         4. als meerdere opties de beste zijn: kies random 1 van deze opties
    #     '''
        
    #     # Return Self of niet???
    #     return i, positionX, positionY

    def get_best_fold(self, protein):
        '''
        Find the best folding for the next amino acid.
        '''
        self.best = []

        # Acquire list of all foldings to try
        fold_list = self.get_fold_list()

        # TODO
        # Fix even de previous fold indexatie (*-1)
        fold_list.remove(self.prev_fold)

        # Remove folds from list if in forbidden lists
        acid = protein.aminoacids[self.i]
        for j in len(acid.forbidden_folds):
            if acid.forbidden_folds[j] in fold_list:
                fold_list.remove(acid.forbidden_folds[j])

        # Try all possible foldings and return a random one of the best options
        for _ in fold_list:
            folding = fold_list.pop()
            temp_fold = self.get_temp_coordinates(folding)
            positionX, positionY = self.try_fold(protein, temp_fold)

            if positionX:
                protein.add_position(protein.aminoacids[self.i], positionX, positionY)
                self.add_best(protein, folding)
            else:
                pass

        return random.choice(self.best)

    
    def try_fold(self, protein, temp_fold):
        '''
        Make a temporary fold of an aminoacid and return temporary stability score or None if the fold is N.A.
        '''
        positionXb = temp_fold[0]
        positionYb = temp_fold[1]

        # Assume position if X and Y coordinates are not already occupied by a previous acid
        if not (positionXb, positionYb) in protein.positions.keys():
            positionX = positionXb
            positionY = positionYb

            return positionX, positionY
        else:
            return None, None


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

    
    def add_best(self, protein, folding):
        '''
        Adds stability folding for next aminoacid to temporary list self.best, if best
        '''
        protein.set_stability()
        copy_score = copy.deepcopy(protein.score)

        # Check if this folding gains a higher stability than previous tries.
        if self.best:    
            for j in len(self.best):
                if copy_score >= self.best[j][0]: 
                    self.best.append([copy_score, folding])
        else:
            self.best.append([copy_score, folding])


    def run_greedy(self, protein, x):
        '''
        Fold the protein according to the greedy algorithm x times.
        '''
        for _ in range(x):

            # Finish a protein with greedy folding
            self.positionX = self.positionY = 0
            self.i = 0
    
            while self.i < len(protein.aminoacids):
                protein.add_position(protein.aminoacids[self.i], self.positionX, self.positionY)
                self.i, self.positionX, self.positionY = self.fold_random(protein, self.positionX, self.positionY, self.i)

            protein.set_stability()
            self.add_solution(protein)


class GreedyLookahead(Greedy):
    pass
