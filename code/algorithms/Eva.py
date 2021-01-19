import copy

# taken from the Radio Russia example

class DepthFirst:
    """
    A Depth First algorithm that builds a stack of graphs with a unique assignment of nodes for each instance.
    """
    def __init__(self, graph, transmitters):
        self.graph = copy.deepcopy(graph)
        self.transmitters = transmitters

        self.states = [copy.deepcopy(self.graph)]

        self.best_solution = None
        self.best_value = float('inf')

    def get_next_state(self):
        """
        Method that gets the next state from the list of states.
        """
        return self.states.pop()

    def build_children(self, graph, node): # graph is protein
        """
        Creates all possible child-states and adds them to the list of states.
        """
        # Retrieve all valid possible values for the node.
        values = node.get_possibilities(self.transmitters) # pos --> folding: 3 options.

        # Add an instance of the graph to the stack, with each unique value assigned to the node.
        for value in values: # go through the foldings
            new_graph = copy.deepcopy(graph) # copy protein, and do a fold
            new_graph.nodes[node.id].set_value(value) # do one folding, looping over all 3 foldings, add the foldings to the stack
            self.states.append(new_graph)

    def check_solution(self, new_graph):
        """
        Checks and accepts better solutions than the current solution.
        """
        new_value = new_graph.calculate_value()
        old_value = self.best_value

        # We are looking for maps that cost less!
        if new_value <= old_value:
            self.best_solution = new_graph
            self.best_value = new_value
            print(f"New best value: {self.best_value}")

    def run(self):
        """
        Runs the algorithm untill all possible states are visited.
        """
        while self.states:
            new_graph = self.get_next_state()

            # Retrieve the next empty node.
            node = new_graph.get_empty_node()

            if node is not None:
                self.build_children(new_graph, node) # adds children of protein
            else:
                # Stop if we find a solution
                # break

                # or ontinue looking for better graph
                self.check_solution(new_graph)

        # Update the input graph with the best result found.
        self.graph = self.best_solution

#------------------------------------------------------------------------------------------------------------->
