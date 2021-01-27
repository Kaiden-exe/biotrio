from .random import Random
from .depth_first import DepthFirst, GreedyDepth
from code.classes.protein import Protein
from code.classes.aminoacid import AminoAcid
import random
import copy

class Greedy(Random):
    """
    A Greedy algorithm that builds a stack of proteins with a unique folding for each instance.
    """
    def __init__(self, protein):
        super().__init__()
        self.protein = protein
        # List of all [Score, Folding] combinations per fold
        self.best_fold = []
        self.positionX = 0
        self.positionY = 0
        self.i = 0


    def fold(self):
        '''
        Returns a specific folding value.
        '''
        folding = self.get_best_fold(self.protein)

        return folding


    def get_best_fold(self, protein):
        '''
        Find the best folding for the next amino acid.
        '''
        self.best_fold = []

        # Acquire list of all foldings to try
        fold_list = Protein.get_fold_list(protein)

        if self.i > 0:
            prev_fold = protein.aminoacids[self.i-1].folding
            fold_list.remove(prev_fold * -1)

        # Remove folds from list if in forbidden lists
        acid = protein.aminoacids[self.i]
        for j in range(len(acid.forbidden_folds)):
            if acid.forbidden_folds[j] in fold_list:
                fold_list.remove(acid.forbidden_folds[j])

        # Try all possible foldings and return a random one of the best options
        for k in range(len(fold_list)):
            folding = fold_list[k]
            temp_fold = self.get_temp_coordinates(folding)
            trial = self.try_fold(protein, temp_fold)

            if trial == True:
                self.add_best(protein, temp_fold)
            else:
                pass
        
        # Return best fold choice, none if no options available to reset of iteration
        if self.best_fold:
            random_best = random.choice(self.best_fold)
        else:
            return None

        new_fold = self.get_temp_coordinates(random_best[1])
        self.positionX = new_fold[0]
        self.positionY = new_fold[1]

        return random_best[1]

    
    def try_fold(self, protein, temp_fold):
        '''
        Make a temporary fold of an aminoacid and return temporary stability score or None if the fold is N.A.
        '''
        positionXb = temp_fold[0]
        positionYb = temp_fold[1]

        # Assume position if X and Y coordinates are not already occupied by a previous amino acid
        if not (positionXb, positionYb) in protein.positions.keys():
            return True
        else:
            return False


    def get_temp_coordinates(self, folding):
        '''
        Returns the coordinates for the next amino according to the temporary folding of the previous amino.
        '''
        # Rotate amino acid over the X-axis
        if folding == 1 or folding == -1:
            yb = self.positionY
            xb = self.positionX + folding

        # Rotate amino acid over the Y-axis
        else:
            xb = self.positionX
            yb = self.positionY + int(folding/2)
        
        return [xb, yb, folding]

    
    def add_best(self, protein, temp_fold):
        # TODO - docstring looks incomplete
        '''
        Adds stability folding for next aminoacid to temporary list self.best, if best
        '''
        positionXb = temp_fold[0]
        positionYb = temp_fold[1]
        folding = temp_fold[2]

        # Save score of the temporary folding to the next amino acid
        temp_protein = copy.deepcopy(protein)
        temp_protein.add_position(protein.aminoacids[self.i+1], positionXb, positionYb)
        temp_protein.set_stability()
        temp_score = temp_protein.score

        del temp_protein

        # Check if this folding gains a higher stability than previous tries
        if self.best_fold:
            if temp_score < self.best_fold[0][0]:
                self.best_fold.clear()
                self.best_fold.append([temp_score, folding])
            else:
                for j in range(len(self.best_fold)):
                    if temp_score == self.best_fold[j][0]:
                        self.best_fold.append([temp_score, folding])
                        break
        else:
            self.best_fold.append([temp_score, folding])


    def run_greedy(self, protein, runs):
        '''
        Fold the protein according to the greedy algorithm x times.
        '''
        for k in range(runs):
            
            # Keep track of progression while running
            if k % 1 == 0:
                print(f"Total number of iterations done: {k}")

            # Finish a protein with greedy folding
            self.positionX = self.positionY = 0
            self.i = 0

            # Loop through a protein and fill in each amino acid per iteration
            while self.i < len(protein.aminoacids):
                protein.add_position(protein.aminoacids[self.i], self.positionX, self.positionY)
                temp_i, temp_positionX, temp_positionY = self.fold_random(protein, self.positionX, self.positionY, self.i)

                # Check if a valid folding is possible, if not retry the previous amino acid with another folding, else continue
                if temp_i == 0:
                    prev_coordinates = protein.remove_last()
                    self.i -= 1
                    self.positionX = prev_coordinates[0]
                    self.positionY = prev_coordinates[1]
                elif type(temp_i) is dict:
                    protein.positions = temp_i
                    break
                else:
                    self.i = temp_i
                    self.positionX = temp_positionX
                    self.positionY = temp_positionY

            protein.set_stability()
            self.add_solution(protein)


class GreedyLookahead(Greedy, GreedyDepth):
    """
    The greedy lookahead algorithm will configure an X amount of amino acids at once
    to calculate a corresponding stability score.
    The first amino acid will be placed according to the best stability score found,
    from where the same pattern will be repeated.
    """
    def __init__(self, protein, lookahead):
        super().__init__(protein)
        self.lookahead = lookahead


    def get_best_fold(self, protein):
        '''
        Get's the best fold for the current amino acid, according to the depth first results.
        '''
        start_state = self.get_start_state()

        # Run depth first with the current folded protein and the lookahead amino's
        depth_first = GreedyDepth(start_state)
        depth_first.run_depthfirst()

        # Isolate information from best result from depth first algorithm
        best_solution = depth_first.get_best_solution()

        if not best_solution:
            return None

        dict_best = best_solution[1]
        best_values = list(dict_best.values())

        # Terminate the depth first early when the last amino acids are positioned.
        if len(dict_best) == len(protein.aminoacids):
            return dict_best

        curr_amino = best_values[-self.lookahead-1]
        
        fold = curr_amino.folding
        del start_state

        return fold


    def get_start_state(self):
        '''
        Initiates first states in the stack for the depth first algorithm.
        '''
        start_state = copy.deepcopy(self.protein)

        # Remove folds from list if in forbidden lists
        acid = start_state.aminoacids[self.i]
        for j in range(len(acid.forbidden_folds)):
            if acid.forbidden_folds[j] in start_state.depth_values:
                start_state.depth_values.remove(acid.forbidden_folds[j])

        # Make sure DepthFirst knows what amino acid should be folded next in the protein 
        start_state.depth_index = self.i

        # self.lookahead amino's + positions isoleren, staart afknippen
        amino_remove = len(start_state.aminoacids) - len(start_state.positions) - self.lookahead

        if amino_remove > 0:
            for _ in range(amino_remove):
                remove = start_state.aminoacids[-1]
                start_state.aminoacids.remove(remove)

        # Return part of the protein for the correct state state in depth first
        return start_state