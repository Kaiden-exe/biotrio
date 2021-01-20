from .hill_climber import HillClimber
import random
import math
import copy

class Simulated_Annealing(HillClimber):
    def __init__(self, protein, initial_temp):
        super().__init__(protein)
        self.initial_temp = initial_temp
        self.alpha = None
        self.current_temp = initial_temp

    def hike(self, iterations, mutations):
        '''
        Runs the simulated annealing algorithm.
        '''

        self.alpha = self.initial_temp / iterations

        for i in range(iterations):
            new = copy.deepcopy(self.best)

            for j in range(mutations):
                self.mutate(new)

            new.set_stability()
            self.add_solution(new)

            if new.score < self.best.score:
                del self.best
                self.best = new
            else:
                diff = self.get_diff(new)
                if random.uniform(0, 1) < math.exp(diff / self.current_temp):
                    del self.best
                    self.best = new
                else:
                    del new
            
            self.update_temp()
    
    def get_diff(self, new):
        score_best = self.best.score
        score_new = new.score
        return abs(score_new - score_best)

    def update_temp(self):
        self.current_temp -= self.alpha
