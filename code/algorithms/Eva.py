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

# example graph
g = {
    'u': ['v', 'x'],
    'v': ['y'],
    'y': ['x'],
    'x': ['v'],
    'w': ['y', 'z'],
    'z': ['z']
    }

# get all positions of the state-space
# in loop: make sure it can't fold in on its self: if statement, if it folds in on itself - don't continue with that route. Do this to avoid
# over-riding of other positions: graph will become inaccurate.
# for every amino.index, make a new option, so that they have a different folding.
# index 0 --> 4 versions

def get_surrounding_coordinates(self, x, y):
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

# starting position: where H's position is 0.0.
# then get the positions of all the possible positions the next amino acid will can be.
# do the same for that amino acid.
g[(0,0)] = protein.get_surrounding_coordinates(0,0)

while len(g) < n^(r-1):

#---------------------------------------------------------------------------------

g = {}

# coordinates 0,0 are the starting position
g[(0,0)] = protein.get_surrounding_coordinates(0,0)

# have to find the position for all options, starting with the surrounding positions of 0,0
# begin with 0,0
for pos in g[(0,0)]:
    g[pos] = protein.get_surrounding_coordinates(pos)

#---------------------------------------------------------------------------------

# an example of what the graph will need to look like
g = {
    (0,0) : protein.get_surrounding_coordinates(0, 0)
}

#---------------------------------------------------------------------------------

# the state-space calculations
n^(r-1)

# n is length of the protein
# r is folding options
n = len(get_fold_list)


# like this??
g = {
    'H' : ['-1', '1', '-2', '2'],
    'P' : [(-1, -1), (-1, 1), ... (2, 2)],
    'H' : [...]
}

# a simple example of what I thought we need to graph
g = {
    '-': ['L', 'R'],
    'L': ['LL', 'LR'],
    'LL': ['LLL', 'LLR'],
    'LR': ['LRL', 'LRR'],
    'R': ['RL', 'RR'],
    'RL': ['RLL', 'RLR'],
    'RR': ['RRL', 'RRR']
}

class depth_first:
    def __init__(self):
        self.visited = []
    
    def dfs(self, graph):        
        for ver in graph:
            if ver not in self.visited:
                self.dfs_visit(graph, ver)

        return self.visited

    def dfs_visit(self, graph, vertex):
        if vertex not in self.visited:
            self.visited.append(vertex)
            for nb in g[vertex]:
                self.dfs_visit(g, nb)


# for testing
d = depth_first()
print(d.dfs(g))

#---------------------------------------------------------------------------------

