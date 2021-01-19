# from code.classes.protein import Protein
from code.algorithms.random import Random
import copy

# taken from the Radio Russia example

class DepthFirst:
    """
    A Depth First algorithm that builds a stack of proteins with a unique assignment of nodes for each instance.
    """
    def __init__(self, protein):
        self.protein = copy.deepcopy(protein)

        self.states = [copy.deepcopy(self.protein)]

        self.best_solution = None
        self.best_value = float('inf')

    def get_next_state(self):
        """
        Method that gets the next state from the list of states.
        """
        return self.states.pop()

    def build_children(self, protein, acid): # graph is protein, is node amino acid?
        """
        Creates all possible child-states and adds them to the list of states.
        """
        # Retrieve all valid possible values for the node.
        # values = node.get_possibilities(self.transmitters) 
        # # pos --> folding: 3 options.

        # values = get_fold_list()
        values = [-1, 1, -2, 2]

        # Add an instance of the graph/protein to the stack, with each unique value assigned to the node/?amino acid?.
        for value in values: # go through the foldings: goes through all 3 foldings
            new_protein = copy.deepcopy(protein) # copy protein, and do a fold
            # do one folding, looping over all 3 foldings, add the foldings to the stack
            # new_graph.nodes[node.id].set_value(value) 

            !!!
            aminoacid.folding = value # does this take just one amino acid per time?
            !!!

            self.states.append(new_protein)

    def check_solution(self, new_protein):
        """
        Checks and accepts better solutions than the current solution.
        """
        # new_value = new_graph.calculate_value()
        new_value = new_protein.set_stability()
        old_value = self.best_value

        # We are looking for maps that cost less!
        # We are looking for the highest stability score!
        if new_value <= old_value:
            # self.best_solution = new_graph
            self.best_solution = new_protein

            self.best_value = new_value
            print(f"New best value: {self.best_value}")

    def run(self):
        """
        Runs the algorithm untill all possible states are visited.
        """ 
        while self.states:
            # new_graph = self.get_next_state()
            new_protein = self.get_next_state()

            # Retrieve the next empty node. # Retrieve the next amino acid????
            node = new_graph.get_empty_node()
            
            if stack < len(protein):
                !!!
                # trying to figure out what to do in relation to the radio russia example
                self.build_children(new_protein)
                !!!
            else:
                break

            # if node is not None:
            #     self.build_children(new_graph, node) # adds children of protein
            # else:
            #     # Stop if we find a solution
            #     # break

            #     # or continue looking for better graph
            #     self.check_solution(new_graph)
            

            if acid is not None:
                self.build_children(new_protein, acid) # adds children of protein
            else:
                # Stop if we find a solution
                # break

                # or continue looking for better graph
                self.check_solution(new_protein)

        # Update the input graph with the best result found.
        self.protein = self.best_solution

#------------------------------------------------------------------------------------------------------------->

