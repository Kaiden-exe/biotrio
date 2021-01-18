import copy

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

    def build_children(self, graph, node):
        """
        Creates all possible child-states and adds them to the list of states.
        """
        # Retrieve all valid possible values for the node.
        values = node.get_possibilities(self.transmitters)

        # Add an instance of the graph to the stack, with each unique value assigned to the node.
        for value in values:
            new_graph = copy.deepcopy(graph)
            new_graph.nodes[node.id].set_value(value)
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
                self.build_children(new_graph, node)
            else:
                # Stop if we find a solution
                # break

                # or ontinue looking for better graph
                self.check_solution(new_graph)

        # Update the input graph with the best result found.
        self.graph = self.best_solution

#-------------------------------------------------------------------------------------------------------->

g = {
    'u': ['v', 'x'],
    'v': ['y'],
    'y': ['x'],
    'x': ['v'],
    'w': ['y', 'z'],
    'z': ['z']
    }

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

# ik snap niet wat ik precies uit de protein moet halen om in me graph te zetten.
