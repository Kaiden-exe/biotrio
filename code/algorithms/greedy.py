from .random import Random
from code.classes.protein import Protein
import random
import copy

class Greedy(Random):
    def __init__(self):
        self.protein = Protein
        # List that contains the coordinates of the best found foldings
        self.best = []
        # List that keeps track of all tried foldings per amino acid
        self.prev_fold = []


    def fold(self):
        '''
        Returns a specific folding value.
        '''
        folding = self.get_best(self.protein)
        self.prev_fold = [folding]

        return folding


    def fold_greedy(self, protein, positionX, positionY, i):
        '''
        1. alle opties fold van volgende aminozuur proberen
            2. van elke optie stability score berekenen
        3. fold returnen van optie met beste stability
            4. als meerdere opties de beste zijn: kies random 1 van deze opties
        '''
        pass

    def get_best(self, protein):
        '''
        Find the best folding for the next amino acid.
        '''
        # Acquire list of all foldings to try
        fold_list = self.get_fold_list()
        fold_list.remove(self.prev_fold)

        for _ in fold_list:
            pass
            # 1. Folding toevoegen aan gevouwen eiwit tot nu toe
            # 2. Stabiliteitsscore berekenen met nieuwe aminozuur
            # 3. Append to best lijst als hoger dan of gelijk aan vorige score

        return random.choice(self.best)

    
    def add_best(self, protein):
        '''
        Adds 'best' stability folding for next aminoacid to temporary list self.best
        '''
        protein.set_stability()
        copy_score = copy.deepcopy(protein.score)
        copy_dict = copy.deepcopy(protein.positions)
        self.best.append([copy_score, copy_dict])


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
                i, positionX, positionY = self.fold_greedy(protein, positionX, positionY, i)

            protein.set_stability()
            self.add_solution(protein)


class GreedyLookahead(Greedy):
    pass
