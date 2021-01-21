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
from .random import Random
from code.classes.protein import Protein
from code.classes.aminoacid import AminoAcid

class DepthFirst:
    """
    A Depth First algorithm that builds a stack of proteins with a unique folding for each instance.
    """
    def __init__(self, protein):
        self.protein = copy.deepcopy(protein)
        # self.states = [copy.deepcopy(self.protein)]
        self.states = []

        # at the moment best_solution and best_stability are still single value
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
        # values are the possible foldings that we can assign to the amino acid
        # TODO
        # fold_list = Random.get_fold_list()
        # failsave for previous amino acid, surroundings acids

        # how do we check what folding the previous amino acid had (what folding the parent had)
        values = [-1, 1, -2, 2]

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
            # Check if new folding does not intersect with rest of protein
            child.depth_index += 1
            child.add_position(child.aminoacids[child.depth_index], x, y)

            # add the child to the stack
            self.states.append(child)
        

    def check_solution(self, new_protein):
        '''
        Checks and accepts better solutions than the current solution.
        '''
        new_protein.set_stability()
        new_stability = new_protein.score

        if new_stability == self.best_stability:

            # Save all best solutions, not only the last one found
            # Make sure to save in dictionary/list, with score + folding

            self.best_solutions.append([self.best_stability, new_protein.positions])
        elif new_stability < self.best_stability:

            self.best_stability = new_stability
            self.best_solutions.clear()

            # copy_dict = copy.deepcopy(new_protein.positions)
            # !!! have to make sure to save score and coordinates !!!
            self.best_solutions.append([new_protein.score, new_protein.positions])
            print(f"new_protein.positions")


    # def get_nofold_amino(self, new_protein):
    #     '''
    #     Returns the first amino acid with no folding.
    #     '''
    #     # where do I get the protein instance from??
    #     for amino in new_protein:
    #         if amino.folding is None:
    #             return amino
        
    #     return None

    
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
        
        print(f"New best solutions: {self.best_solutions}")
        temp_protein = self.best_solutions[1]
        print(f"TEMP_PROTEIN: {temp_protein}")
        self.protein.positions = temp_protein[1]
        self.protein.score = temp_protein[0]


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


    # def create_coordinates(self, protein):
    #     aminos = protein.aminoacids

    #     for amino in aminos:
    #         if amino.folding == None: 
    #             break
    #         # previous coordinates 
    #         # if -1 or 1 -> new_coordinates =  x + folding 
    #         # if -2 or 2 -> new_coordinates = y + folding
