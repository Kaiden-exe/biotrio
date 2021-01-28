from code.classes.aminoacid import AminoAcid
from code.classes.protein import Protein
from .randomize import Random
import copy
import random

class DepthFirst():
    """
    A Depth First algorithm that builds a stack of states of a protein with a unique folding for each state.
    It searches the states to find and return the best solution.
    """
    def __init__(self, protein):
        self.protein = copy.deepcopy(protein)
        self.states = []
        self.sol_dict = {}
        self.best_solutions = []
        self.best_stability = 0


    def get_next_state(self):
        '''
        Method that gets the next state from the list of states.
        '''
        return self.states.pop()


    def build_children(self, curr_state):
        '''
        Creates all possible child-states and adds them to the list of states.
        '''
        # Retreive the folding of the last folded amino acid
        last_folding = curr_state.aminoacids[curr_state.depth_index-1].folding
        
        # Makes sure the amino acid does not fold back on itself
        if last_folding is not None:
            last_folding *= -1
            if last_folding in curr_state.depth_values:
                curr_state.depth_values.remove(last_folding)

        # Get the next folding (value) from the possible foldings
        if curr_state.depth_values:
            value = curr_state.depth_values.pop()
            self.states.append(curr_state)

            # Make children if folding values are available
            if value is not None:
                child = copy.deepcopy(curr_state)

                # Assign the value to the amino acid's folding 
                child.aminoacids[child.depth_index].folding = value
                
                x, y = self.get_coordinates(value, child)

                # If the child makes invalid folds, delete the child
                if (x, y) in child.positions.keys():
                    del child
                else:
                    # Check if new folding does not intersect with the rest of protein
                    child.depth_index += 1
                    child.add_position(child.aminoacids[child.depth_index], x, y)

                    # Add the child to the stack
                    child.depth_values = child.get_fold_list()
                    self.states.append(child)
        else:
            del curr_state


    def check_solution(self, new_protein):
        '''
        Checks and accepts better solutions than the current solution, or save equally good ones.
        '''
        new_protein.set_stability()
        new_stability = new_protein.score

        # Count all found stability scores
        if new_protein.score in self.sol_dict.keys():
            self.sol_dict[new_protein.score] += 1
        else:
            self.sol_dict[new_protein.score] = 1

        # Check if solution is better than previous solutions, if so overwrite it
        if new_stability < self.best_stability or not self.best_solutions:
            self.best_stability = new_stability
            self.best_solutions.clear()
            self.best_solutions.append([new_protein.score, new_protein.positions])
        
        # If the solution is equal to previous best solutions, append it to the list
        elif new_stability == self.best_stability:
            self.best_solutions.append([new_protein.score, new_protein.positions])

        del new_protein


    def get_coordinates(self, folding, child):
        '''
        Returns the coordinates for the next amino acid according to the folding of the previous one.
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
        Returns the best solution from all generated solutions, return None if no solutions are found.
        '''
        print(f"list: {self.best_solutions}")
        if self.best_solutions:
            best = random.choice(self.best_solutions)
        else:
            best = None
        print(f"best: {best}")

        return best
            

    def run_depthfirst(self):
        '''
        Runs the algorithm untill all possible states are visited.
        '''
        self.initiate()

        while self.states:
            curr_state = self.get_next_state()
            
            # If we are at the end of the protein, check stability, otherwise build children
            if curr_state.depth_index + 1 == len(self.protein.aminoacids):
                self.check_solution(curr_state)
            else:
                self.build_children(curr_state)


    def initiate(self):
        '''
        Initiates first states in the stack.
        '''
        # Initiate the first 2 foldings of the protein and the last amino acid
        self.protein.aminoacids[0].folding = 1
        self.protein.aminoacids[1].folding = 1
        self.protein.aminoacids[-1].folding = 0

        # Initiate coordinates of the first 2 amino acids
        self.protein.add_position(self.protein.aminoacids[0], 0, 0)
        self.protein.add_position(self.protein.aminoacids[1], 1, 0)
        self.protein.depth_index = 2

        # Initiate both 2 options of coordinates for the 3rd amino acid
        self.protein.add_position(self.protein.aminoacids[2], 2, 0)
        self.protein.aminoacids[2].folding = 1
        start_state1 = copy.deepcopy(self.protein)
        self.protein.remove_last()

        self.protein.add_position(self.protein.aminoacids[2], 1, 1)
        self.protein.aminoacids[2].folding = 2
        start_state2 = copy.deepcopy(self.protein)
        
        # Add start states to the stack
        self.states.append(start_state1)
        self.states.append(start_state2)


class GreedyDepth(DepthFirst):
    '''
    DepthFirst algorithm, specific for running the GreedyLookahead algorithm.
    '''
    def __init__(self, protein):
        super().__init__(protein)
        self.states = [protein]


    def initiate(self):
        '''
        Skip original initiation of states from DepthFirst.
        '''
        pass