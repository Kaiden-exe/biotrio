import copy
# from .random import Random
from code.classes.protein import Protein
from code.classes.aminoacid import AminoAcid
from code.algorithms.random import Random
import random

class DepthFirst():
    """
    A Depth First algorithm that builds a stack of proteins with a unique folding for each instance.
    """
    def __init__(self, protein):
        self.protein = copy.deepcopy(protein)
        self.states = []
        self.solutions = []
        self.best_solutions = []
        self.best_stability = 0


    def get_next_state(self):
        '''
        Method that gets the next state from the list of states.
        '''
        return self.states.pop()


    def build_children(self, new_protein):
        '''
        Creates all possible child-states and adds them to the list of states.
        '''
        # how do we check what folding the previous amino acid had (what folding the parent had)
        values = Protein.get_fold_list(self.protein)

        # don't let it fold back onto itself
        parent = new_protein
        last_folding = parent.aminoacids[parent.depth_index].folding

        if last_folding is not None:
            last_folding = last_folding * -1
            values.remove(last_folding)

        # we give the amino acid the different folding options that it can have
        for value in values:
            child = copy.deepcopy(parent)

            # assign the value to the amino acid's folding (using the aminoacid defined above)
            child.aminoacids[child.depth_index].folding = value
            
            x, y = self.get_coordinates(value, child)

            # if a child becomes a parent, the possible values of its offspring cannot b
            # an attribute that keeps track of what the childrens values can or cannot be.
            # neighbours = child.get_surrounding_coordinates(x, y)

            if (x, y) in child.positions.keys():
                del child
            else:
                # Check if new folding does not intersect with rest of protein
                child.depth_index += 1
                child.add_position(child.aminoacids[child.depth_index], x, y)
            
                # Add the child to the stack
                self.states.append(child)

        # TODO ########################
        # del parent (of new_protein?)


    def check_solution(self, new_protein):
        '''
        Checks and accepts better solutions than the current solution, or save equally good ones.
        '''
        new_protein.set_stability()
        new_stability = new_protein.score
        
        # Add solution to the list
        self.solutions.append([new_protein.score, new_protein.positions])

        # Check if solution is better or equal to previous solutions
        if new_stability == self.best_stability:
            self.best_solutions.append([self.best_stability, new_protein.positions])
            # TODO ##############################
            # del new_protein

        elif new_stability < self.best_stability:

            self.best_stability = new_stability
            # TODO ###############################
            # del new_protein

            self.best_solutions.clear()
            self.best_solutions.append([new_protein.score, new_protein.positions])


    def get_coordinates(self, folding, child):
            '''
            Returns the coordinates for the next amino according to the folding of the previous amino.
            '''
            coordinates = child.positions.keys()
            for x, y in coordinates:
                prev_x = x
                prev_y = y

            # Rotate amino acid over the X-axis
            if folding == 1 or folding == -1:
                yb = prev_y
                xb = prev_x + folding

            # Rotate amino acid over the Y-axis
            else:
                xb = prev_x
                yb = prev_y + int(folding/2)
            
            return [xb, yb]


    def get_best(self):
        '''
        Returns a random best solution from all generated best solutions.
        '''
        # Choose a random best solution
        best = random.choice(self.best_solutions)

        return best
            

    def run(self):
        '''
        Runs the algorithm untill all possible states are visited.
        '''      
        # Initiate coordinates of the first amino acid 
        self.protein.add_position(self.protein.aminoacids[0], 0, 0)
        self.states.append(self.protein)

        # while the stack is not empty
        while self.states:
            # we got a protein out of the states: the parent
            new_protein = self.get_next_state()
            
            # when there are no more foldings to do, remember what the stability score is
            if new_protein.depth_index+1 == len(self.protein.aminoacids):
                self.check_solution(new_protein)
            else:
                self.build_children(new_protein)

            # TODO ##############################
            # del new_protein
        
        # Fill original protein class with a best solution to visualize this data
        final_solution = random.choice(self.best_solutions)
        self.protein.positions = final_solution[1]
        self.protein.score = final_solution[0]