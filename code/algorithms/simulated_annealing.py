from .hill_climber import HillClimber, HillClimber_Pull
import copy
from math import exp
import random

class Simulated_Annealing(HillClimber):
    '''
    Simulated annealing algorithm that uses the single mutation hill climber. 
    '''
    def __init__(self, protein, initial_temp, runs):
        self.initial_temp = initial_temp
        self.alpha = initial_temp / runs
        self.current_temp = initial_temp
        super().__init__(protein, runs)


    def accept(self, new):
        '''
        Returns whether a mutated protain with an equal or worse score gets accepted.
        '''
        diff = abs(self.best.score) - abs(new.score)
        acceptance_chance = exp(-diff / self.current_temp)
        if random.uniform(0,1) < acceptance_chance:

            return True
            
        return False


    def update_temp(self):
        '''
        Updates the current temperature.
        '''
        self.current_temp -= self.alpha

    
    def add_solution(self, protein):
        '''
        Tallies the solution scores.
        '''
        # Count all found stability scores
        if protein.score in self.sol_dict.keys():
            self.sol_dict[protein.score] += 1
        else:
            self.sol_dict[protein.score] = 1
        
        self.update_temp()


class Simulated_Annealing_Pull(Simulated_Annealing, HillClimber_Pull):
    '''
    Simulated annealing algorithm that uses the pull move mutation hill climber. 
    '''
    pass