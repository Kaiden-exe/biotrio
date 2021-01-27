from .hill_climber import HillClimber, HillClimber_Pull
import random
import math
import copy

class Simulated_Annealing(HillClimber):
    # TODO - add docstring
    '''
    '''
    def __init__(self, protein, initial_temp, runs):
        self.initial_temp = initial_temp
        self.alpha = initial_temp / runs
        self.current_temp = initial_temp
        super().__init__(protein, runs)


    def accept(self, new):
        # TODO - add docstring
        '''
        '''
        diff = abs(self.best.score) - abs(new.score)
        acceptance_chance = math.exp(-diff / self.current_temp)
        if random.uniform(0,1) < acceptance_chance:
            return True
        return False


    def update_temp(self):
        # TODO - add docstring
        '''
        '''
        self.current_temp -= self.alpha

    
    def add_solution(self, protein):
        '''
        Add a solution to the list of solutions.
        '''
        # TODO: turn into dictionary 
        score = protein.score
        self.solutions.append(score)
        self.update_temp()

class Simulated_Annealing_Pull(Simulated_Annealing, HillClimber_Pull):
    # TODO: doc string 
    pass