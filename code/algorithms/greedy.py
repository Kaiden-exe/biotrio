from code.classes.aminoacid import AminoAcid
from code.classes.protein import Protein
from .depth_first import DepthFirst, GreedyDepth
from .randomize import Random
import copy
import random

class Greedy(Random):
    """
    Greedy algorithm, which chooses foldings based on the scores that all possible foldings create. 
    """
    def __init__(self, protein):
        super().__init__()
        self.protein = protein
        self.best_fold = []
        self.positionX = 0
        self.positionY = 0
        self.index = 0


    def fold(self):
        '''
        Finds the best folding for the next amino acid.
        '''
        self.best_fold = []
        fold_list = self.protein.get_fold_list()

        # Make sure the amino acid does not fold back on itself
        if self.index > 0:
            prev_fold = self.protein.aminoacids[self.index-1].folding
            fold_list.remove(prev_fold * -1)
        else:

            return random.choice(fold_list)

        acid = self.protein.aminoacids[self.index]

        # Remove possible folds from list if present in forbidden folds list of the amino acid
        for fold in acid.forbidden_folds:
            if fold in fold_list:
                fold_list.remove(fold)

        # Try all folds available
        for fold in fold_list:
            temp_fold = self.get_temp_coordinates(fold)

            # If the fold is valid, add it to solutions
            if self.try_fold(self.protein, temp_fold):
                self.add_best(self.protein, temp_fold)
        
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
        Checks the fold for an amino acid and returns True if the fold is valid.
        '''
        positionX = temp_fold[0]
        positionY = temp_fold[1]

        # Check if coordinates are not already occupied by a previous amino acid
        if not (positionX, positionY) in protein.positions.keys():
            
            return True
            
        return False


    def get_temp_coordinates(self, folding):
        '''
        Returns the coordinates for the next amino according to the temporary folding of the previous amino acid.
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
        '''
        Adds stability score after folding the next amino acid to temporary list self.best, 
        if equal to or better than previous stability scores.
        '''
        positionXb = temp_fold[0]
        positionYb = temp_fold[1]
        folding = temp_fold[2]

        # Save score of the temporary folding to the next amino acid
        temp_protein = copy.deepcopy(protein)
        temp_protein.add_position(protein.aminoacids[self.index + 1], positionXb, positionYb)
        temp_protein.set_stability()
        temp_score = protein.score

        del temp_protein

        # Check if this folding has a stability score better than or equal to previous tries
        if self.best_fold:
            if temp_score < self.best_fold[0][0]:
                self.best_fold.clear()
                self.best_fold.append([temp_score, folding])
            elif temp_score == self.best_fold[0][0]:
                self.best_fold.append([temp_score, folding])
        else:
            self.best_fold.append([temp_score, folding])


    def run_greedy(self, protein, runs):
        '''
        Fold the protein according to the greedy algorithm x times.
        '''
        for k in range(runs):
            
            # Keep track of progression while running
            if k % 10 == 0:
                print(f"Total number of iterations done: {k}")

            # Reset global values as initiation for next iteration
            self.positionX = self.positionY = 0
            self.index = 0

            # Loop through a protein and fill in each amino acid per iteration
            while self.index < len(protein.aminoacids):
                protein.add_position(protein.aminoacids[self.index], self.positionX, self.positionY)
                temp_index, temp_positionX, temp_positionY = self.fold_random(protein, self.positionX, self.positionY, self.index)

                # Check if a valid folding is possible, if not retry the previous amino acid with another folding
                if temp_index == 0:
                    prev_coordinates = protein.remove_last()
                    self.index -= 1
                    self.positionX = prev_coordinates[0]
                    self.positionY = prev_coordinates[1]

                # For GreedyLookahead, return final dict positions and proceed to next iteration
                elif type(temp_index) is dict:
                    break

                # Update global parameters and continue with next amino acid
                else:
                    self.index = temp_index
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


    def fold(self):
        '''
        Get's the best fold for the current amino acid, according to the depth first results.
        '''
        start_state = self.get_start_state()

        # Run depth first with the current folded protein and the lookahead amino's
        depth_first = GreedyDepth(start_state)
        depth_first.run_depthfirst()

        # Isolate information from best result from depth first algorithm
        best_solution = depth_first.get_best()

        if not best_solution:

            return None

        dict_best = best_solution[1]
        best_values = list(dict_best.values())

        # Terminate the depth first early when the last amino acids are positioned
        if len(dict_best) == len(self.protein.aminoacids):

            return dict_best

        # Isolate folding of the amino acid with an index equal to self.index
        curr_amino = best_values[-self.lookahead - 1]
        fold = curr_amino.folding
        del start_state

        return fold


    def get_start_state(self):
        '''
        Initiates first states in the stack for the depth first algorithm.
        '''
        start_state = copy.deepcopy(self.protein)

        # Remove folds from list if in forbidden lists
        acid = start_state.aminoacids[self.index]
        for fold in acid.forbidden_folds:
            if fold in start_state.depth_values:
                start_state.depth_values.remove(fold)

        # Make sure DepthFirst knows what amino acid should be folded next in the protein 
        start_state.depth_index = self.index

        # Take out the end of the protein where depth first doesn't have to look yet
        amino_remove = len(start_state.aminoacids) - len(start_state.positions) - self.lookahead

        if amino_remove > 0:
            for _ in range(amino_remove):
                remove = start_state.aminoacids[-1]
                start_state.aminoacids.remove(remove)

        # Return part of the protein for the correct state state in depth first
        return start_state