from .random import Random
from random import choice

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
        for i in range(iterations):
            new_best = self.mutate()
            if new_best[0] < self.best[0]:
                self.best = new_best
    
    def mutate(self):
        aminoacid = choice(self.protein_index)
        folding = get_new_folding(aminoacid)

    def get_new_folding(self, aminoacid):
        folding = aminoacid.folding

        while folding == aminoacid.folding:
            folding = choice(self.get_fold_list())
        


        



