from code.classes.protein import Protein
from .randomize import Random
import copy
from random import choice, getrandbits

class HillClimber(Random):
    '''
    Hill Climber algorithm that compares proteins with a single mutation.
    '''
    def __init__(self, protein, runs):
        super().__init__()
        self.best = self.get_start(protein)
        self.iterations = runs


    def get_start(self, protein):
        '''
        Returns a randomly folded protein to start with.
        '''
        self.run_random(protein, 1)
        self.add_solution(protein)

        return protein
    

    def hike(self, mutations):
        '''
        Runs the hill climber algorithm with i amount of iterations and j amount of mutations per iteration.
        '''

        for i in range(self.iterations):
            new = copy.deepcopy(self.best)

            for j in range(mutations):
                self.mutate(new)

            new.set_stability()
            self.add_solution(new)

            # Compare scores after mutating
            if new.score < self.best.score:
                del self.best
                self.best = new
            elif self.accept(new):
                del self.best
                self.best = new
            else:
                del new 

    
    def accept(self, new):
        '''
        Gives a 50/50 chance that a protein with an equal score gets accepted.
        '''
        if new.score == self.best.score and getrandbits(1):
            return True

        return False
    

    def mutate(self, protein):
        '''
        Changes the coordinates of a single amino acid.
        '''
        # New coordinates will be assigned to a random amino acid
        new_coordinates = ()
        while len(new_coordinates) == 0: 
            
            # Choose a random amino acid from the protein and get all surronding coordinates (exclude last amino acid)
            first_amino = protein.aminoacids[-1]
            while first_amino == protein.aminoacids[-1]:
                amino_coordinates = choice(list(protein.positions.keys()))
                first_amino = protein.positions[amino_coordinates]
            surrounding_coordinates = protein.get_surrounding_coordinates(amino_coordinates[0], amino_coordinates[1])
            
            # Add all surrounding coordinates that are unoccupied to a list
            free_coordinates = self.get_free_coordinates(protein, surrounding_coordinates)
            
            # Check if any of the free coordinates is between the chosen amino acid and two amino acids over
            if len(free_coordinates) > 0:
                try:
                    third_amino = protein.aminoacids[first_amino.index + 2]
                except IndexError: 
                    
                    # You can pick any folding for the last amino acid
                    third_amino = None
                    new_coordinates = choice(free_coordinates) 
                    break
                
                # Check all free coordinates and see if any are adjacent to the third amino acid
                for coordinates in free_coordinates:
                    new_coordinates = self.find_third_aminoacid(protein, third_amino, coordinates)
        
        # Change coordinates of second amino acid and adjust foldings
        second_amino = protein.aminoacids[first_amino.index + 1] 
        self.change_coordinates(protein, second_amino, new_coordinates)
        self.change_folding(protein, first_amino, new_coordinates)
        
        # Repeat if there is also a third amino acid
        if third_amino:
            sorted_postitions = protein.get_sorted_positions()
            third_cor = sorted_postitions[third_amino.index][0]
            self.change_folding(protein, second_amino, third_cor)
        

    def get_free_coordinates(self, protein, surrounding_coordinates):
        '''
        Looks at the surrounding coordinates and returns a list of coordinates that are unoccupied.
        '''
        free_coordinates = []
        for coordinates in surrounding_coordinates:
            if coordinates not in protein.positions.keys():
                free_coordinates.append(coordinates)
        
        return free_coordinates

    
    def find_third_aminoacid(self, protein, third_amino, coordinates):
        '''
        Looks at coordinates and tries to find the third amino acid in the surrounding coordinates.
        If third amino acid is present, coordinates are returned.
        '''
        surrounding_coordinates = protein.get_surrounding_coordinates(coordinates[0], coordinates[1])
        for cor in surrounding_coordinates:
            if cor in protein.positions.keys():
                amino = protein.positions[cor]
            else:
                amino = None

            if amino == third_amino:

                return coordinates
        
        return ()


    def change_coordinates(self, protein, aminoacid, coordinates):
        '''
        Changes the coordinates of an amino acid to the given coordinates.
        '''
        sorted_by_index = protein.get_sorted_positions()
        old_cor = sorted_by_index[aminoacid.index][0]
        del protein.positions[old_cor]
        protein.positions[coordinates] = aminoacid


    def change_folding(self, protein, aminoacid, next_coordinates):
        '''
        Deduces the folding of an amino acid according to the coordinates of the next amino acid.
        '''
        # Get the amino acid coordinates and the coordinates around it 
        lst = protein.get_sorted_positions()
        position = lst[aminoacid.index][0]
        surrounding_coordinates = protein.get_surrounding_coordinates(position[0], position[1])
        folds = protein.get_fold_list()

        # Find fold for amino acid
        for i in range(len(surrounding_coordinates)):
            if surrounding_coordinates[i] == next_coordinates:
                folding = folds[i]
                break

        aminoacid.folding = folding


    def add_solution(self, protein):
        '''
        Tallies the solution scores.
        '''
        # Count all found stability scores
        if protein.score in self.sol_dict.keys():
            self.sol_dict[protein.score] += 1
        else:
            self.sol_dict[protein.score] = 1


    def get_best(self):
        '''
        Returns a list of score and a dictionary of the best found folding.
        '''
        return [self.best.score, self.best.positions]


class HillClimber_Pull(HillClimber):
    '''
    Hill Climber algorithm that compares proteins using the pull move to mutate.
    '''
    def __init__(self, protein, runs):
        super().__init__(protein, runs)
        self.success = 0


    def hike(self):
        '''
        Runs the hill climber pull algorithm with i amount of iterations.
        '''
        for _ in range(self.iterations):
            new = copy.deepcopy(self.best)
            success = self.mutate(new)

            if success:
                self.success += 1
                new.set_stability()
                self.add_solution(new)

                # Compare scores of successful pulls
                if new.score < self.best.score:
                    del self.best
                    self.best = new
                elif self.accept(new):
                    del self.best
                    self.best = new
                else:
                    del new 
            else:
                del new

        print(f"{self.success} out of {self.iterations} mutations were successful")


    def mutate(self, protein):
        '''
        Tries the pull move, and returns whether it was successful or not.
        '''
        # TODO: change i, i_min and i_plus to first, second and third amino EN ALLE ANDERE NEPPE VARIABEL NAMEN
        original_positions = protein.get_sorted_positions()
        
        # Pick random amino acid, but not the first
        third_amino = protein.aminoacids[0]
        while third_amino == protein.aminoacids[0]:
            third_amino = choice(protein.aminoacids)
        third_amino_cor = original_positions[third_amino.index][0]

        # Get the second amino acid
        second_amino = protein.aminoacids[third_amino.index - 1]
        second_amino_cor = original_positions[second_amino.index][0]

        # Get free coordinates of third amino acid
        surrounding_coordinates = protein.get_surrounding_coordinates(third_amino_cor[0], third_amino_cor[1])
        free_coordinates = self.get_free_coordinates(protein, surrounding_coordinates)

        # Move was unsuccessful when there is nowhere to pull to
        if len(free_coordinates) == 0:
            
            return False

        # If second amino acid is the first amino acid of the protein, pull anywhere
        if i.index == 0:
            loc_L = choice(free_coordinates)
            self.change_coordinates(protein, second_amino, loc_L)
            self.change_folding(protein, second_amino, third_amino_cor)

            return True
         
        # TODO - Change L and C to loc_L and loc_C
        # Pull if possible and return if successful or not 
        for loc_L in free_coordinates:
            loc_C = self.get_C(second_amino_cor, third_amino_cor, loc_L)

            if loc_C in protein.positions.keys():

                # Move second amino acid to position L
                if protein.positions[loc_C] == protein.aminoacids[second_amino.index - 1]:
                    self.change_coordinates(protein, second_amino, loc_L)
                    self.change_folding(protein, second_amino, third_amino_cor)
                    self.change_folding(protein, protein.aminoacids[second_amino.index - 1], loc_L)
                    
                    return True
            else: 
                # Move second amino acid to loc_L and first to loc_C
                self.change_coordinates(protein, second_amino, loc_L)
                self.change_folding(protein, second_amino, third_amino_cor)
                first_amino = protein.aminoacids[second_amino.index - 1]
                self.change_coordinates(protein, first_amino, loc_C)
                self.change_folding(protein, first_amino, loc_L)

                # See if the previous amino acid is in the surrounding coordinates
                prev = protein.aminoacids[first_amino.index - 1]
                surrounding_acids = protein.get_surrounding_acids(loc_C[0], loc_C[1])

                # If i - 2 not next to C, keep pulling until the chain is back together
                if not prev in surrounding_acids:
                    self.pull(protein, first_amino, prev, surrounding_acids, original_positions)

                return True
        
        return False


    def pull(self, protein, first, prev, surrounding_acids, original_positions):
        '''
        Keeps pulling until the chain can be linked back together or the last amino acid is reached.
        '''
        backwards_index = first.index

        # Pull until the chain is back together
        while not prev in surrounding_acids and prev.index < backwards_index:
            
            # Pull the previous amino acid in the chain
            next_cor = original_positions[backwards_index][0]
            self.change_coordinates(protein, prev, next_cor)

            # Change the folding of that same amino acid
            sorted_lst = protein.get_sorted_positions()
            next_acid_cor = sorted_lst[prev.index + 1][0]
            self.change_folding(protein, prev, next_acid_cor)

            # Get parameters to check if the chain is back together
            prev = protein.aminoacids[prev.index - 1]
            surrounding_acids = protein.get_surrounding_acids(next_cor[0], next_cor[1])
            backwards_index -= 1

        # Change the fold of the final amino acid
        if prev != protein.aminoacids[-1]:
            self.change_folding(protein, prev, next_cor)
           

    def get_C(self, point_A, point_B, point_L):
        '''
        Finds the fourth point (point C) in the square ABL.
        '''
        delta_x = point_L[0] - point_B[0]
        delta_y = point_L[1] - point_B[1]
        Cx = point_A[0] + delta_x
        Cy = point_A[1] + delta_y
        point_C = (Cx, Cy)

        return C