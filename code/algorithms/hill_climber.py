from .random import Random
from random import choice
import copy

class HillClimber(Random):
    def __init__(self):
        super().__init__()
        self.protein = protein
        self.best = self.get_start()
        self.protein_index = [i for i in range(len(protein.aminoacids))]

    def get_start(self):
        self.run_random(self.protein, 1)
        return self.solutions[0]
    
    def hike(self, iterations):
        '''
        Runs the hill climber algorithm.
        '''
        for i in range(iterations):
            new = self.mutate()
            if new[0] < self.best[0]:
                self.best = new
    
    def mutate(self, protein):
        aminoacid_index = choice(self.protein_index)
        aminoacid = self.protein.aminoacids[aminoacid_index]
        folding = get_new_folding(aminoacid)

    def get_new_folding(self, aminoacid):
        folding = aminoacid.folding

        while folding == aminoacid.folding:
            folding = choice(self.get_fold_list())
        
        return folding
        


        



