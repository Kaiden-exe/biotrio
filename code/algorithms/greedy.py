from .random import Random
import random

class Greedy(Random):
    def __init__(self):
        self.protein = protein
        self.best = []
        self.prev_fold = []


    def fold(self):
        '''
        Folds a protein randomly.
        '''
        fold_list = self.get_fold_list()

        for _ in range(len(self.prev_fold)):
            if self.prev_fold in fold_list:
                fold_list = fold_list.remove(self.prev_fold)

        folding = random.choice(fold_list)

        return folding


    def fold_greedy(self, protein):
        '''
        1. alle opties fold van volgende aminozuur proberen
            2. van elke optie stability score berekenen
        3. fold returnen van optie met beste stability
            4. als meerdere opties de beste zijn: kies random 1 van deze opties
        '''
        pass

    
    def get_new_coordinates(self, x, y):
        '''
        Returns the coordinates for the next aminoacid according to the folding of the previous amino acid.
        '''
        # Chooses a random fold over the x-axis (-1, 1) or the y-axis (-2, 2).
        folding = self.fold()
        
        # Rotate amino acid over the X-axis
        if folding == 1 or folding == -1:
            yb = y
            xb = x + folding

        # Rotate amino acid over the Y-axis
        else:
            xb = x
            yb = y + int(folding/2)
        
        return [xb, yb, folding]


    def get_best(self, protein):
        '''
        Find the best folding for the next amino acid.
        '''
        pass


    def run_greedy(self, protein, x):
        '''
        Fold the protein according to the greedy algorithm x times.
        '''
        for _ in range(x):

            # Finish a protein with greedy folding 
            positionX = positionY = 0
            i = 0
    
            while i < len(protein.aminoacids):
                protein.add_position(protein.aminoacids[i], positionX, positionY)
                i, positionX, positionY = self.fold_greedy(protein)

            protein.set_stability()
            self.add_solution(protein)


class GreedyLookahead(Greedy):
    pass
