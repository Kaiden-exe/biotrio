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
                if self.accept(new):
                    del self.best
                    self.best = new
                else:
                    del new
            
            self.update_temp()
    
    def accept(self, new):
        diff = abs(self.best.score) - abs(new.score)
        acceptance_chance = math.exp(-diff / self.current_temp)
        if random.uniform(0,1) < acceptance_chance:
            return True
        return False

    def update_temp(self):
        self.current_temp -= self.alpha
