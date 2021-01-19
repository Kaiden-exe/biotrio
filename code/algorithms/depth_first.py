'''
Maak lege stack
Voeg eerste staat toe op stack
Herhaal tot stack leeg is:
    Paak bovenste staat op de stack
    Kies eerstvolgende node
    Als we een node hebben:
        Creer nieuwe staten voor elk mogelijke keuze voor node
    Anders:
        klaar?
'''
import copy

class DepthFirst:
    """
    A Depth First algorithm that builds a stack of proteins with a unique folding for each instance.
    """
    def __init__(self, protein):
        self.protein = copy.deepcopy(protein)

        self.states = [copy.deepcopy(self.protein)]

        # at the moment best_solution and best_stability are still single value
        self.best_solution = None
        self.best_stability = 0


    def get_next_state(self):
        '''
        Method that gets the next state from the list of states.
        '''
        return self.states.pop()


    def build_children(self, new_protein, aminoacid):
        '''
        Creates all possible child-states and adds them to the list of states.
        '''
        # values are the possible foldings that we can assign to the amino acid
        values = [-1, 1, -2, 2]

        # we give the amino acid the different folding options that it can have
        for value in values:
            child = copy.deepcopy(new_protein)

            # assign the value to the amino acid's folding (using the aminoacid defined above)
            child.aminoacid.folding = value 

            # add the child to the stack
            self.states.append(child)


    def check_solution(self, new_protein):
        '''
        Checks and accepts better solutions than the current solution.
        '''
        new_stability = new_protein.set_stability()
        if new_stability >= self.best_stability:
            self.best_stability = new_stability
            self.best_solution = new_protein
            print(f"New best stability score: {self.best_stability}")

    
    def run(self):
        '''
        Runs the algorithm untill all possible states are visited.
        '''
        # while the stack is not empty
        while self.states:
            # we got a protein out of the states: the parent
            new_protein = self.get_next_state()

            # we look in our parent and we find the first amino acid without a folding
            aminoacid = new_protein.get_nofold_amino()
            
            # when there are no more foldings to do, remember what the stability score is
            if aminoacid is None:
                self.check_solution(new_protein)
            else:
                self.build_children(new_protein, aminoacid)
           
        # when we are done, override the protein with the best result that has been found
        self.protein = self.best_solution

       
