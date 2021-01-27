from .aminoacid import AminoAcid
import csv

class Protein():
    '''
    Class that holds all information about a protein in its current state. Protein can 
    '''
    def __init__(self, source, protein_id):
        self.id = protein_id
        self.aminoacids = self.load_proteins(source, protein_id)
        self.score = 0
        self.positions = {}
        self.depth_index = 0
        self.depth_values = self.get_fold_list()


    def load_proteins(self, source, protein_id):
        '''
        Takes a csv file and returns a list with proteins.
        '''
        proteins = {}
        with open(source, 'r') as data:
            reader = csv.reader(data)
            next(reader)
            for row in reader:
                proteins[row[0]] = row[1]

        return self.load_acids(proteins[protein_id])


    def load_acids(self, aminos):
        '''
        Returns a list of aminoacids from a string.
        '''
        acidlist = []
        index = 0
        
        for acid_id in aminos:
            amino = AminoAcid(acid_id, index)
            acidlist.append(amino)
            index += 1

        return acidlist


    def add_position(self, acid, x, y):
        '''
        Add the coordinates of a specific amino acid to positions dictionary.
        '''
        self.positions[(x, y)] = acid


    def set_stability(self):
        '''
        Analyses folded protein for H/H or H/C bonds and returns stability.
        '''
        coordinates = self.positions.keys()
        stability = 0
        
        # Loop over all placed amino acids
        for x, y in coordinates:
            acid = self.positions[(x, y)]

            # Check that only H and C form bonds with each other
            if acid.id != 'P':
                surrounding_aminos = self.get_surrounding_acids(x, y)
                
                # TODO: Do this smarter
                # Add stability scores accordingly
                for surround in surrounding_aminos:
                    if surround.index > acid.index + 1 and surround.id != 'P':
                        if 'H' in [surround.id, acid.id]:
                            stability -= 1
                        else:
                            stability -= 5
                        # if surround.id == 'C' and acid.id == 'C':
                        #     stability -= 5
                        # elif acid.id == 'H' and surround.id == 'H':
                        #     stability -= 1
                        # elif acid.id == 'C' and surround.id == 'H':
                        #     stability -= 1
                        # elif acid.id == 'H' and surround.id == 'C':
                        #     stability -= 1

        self.score = stability


    def remove_last(self):
        '''
        Removes the amino acid with the highest index number from positions
        and adds the folding of the second to last amino acid to a list of forbidden folds.
        Returns the coordinates of the second to last amino acid.
        '''
        # Create a list, sorted by index and take the highest
        lst = self.positions.items()
        sorted_by_index = sorted(lst, key=lambda x: x[1].index)
        last = sorted_by_index.pop()

        # Delete last added amino acid from positions
        position = last[0]
        acid = last[1]
        acid.forbidden_folds.clear()
        del self.positions[position]

        # Add the folding of the second to last to a list of forbidden folds
        second = sorted_by_index.pop()
        acid = second[1]
        acid.forbidden_folds.append(acid.folding)
        
        return second[0]


    def get_fold_list(self):
        '''
        Returns a list of all possible foldings.
        '''
        return [-1, 1, -2, 2]


    def get_surrounding_coordinates(self, x, y):
        # TODO: Change so you can just insert a tuple 
        # TODO - add docstring
        '''
        Returns the coordinates surrounding the specified amino acid.
        '''
        return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


    def get_surrounding_acids(self, x, y):
        # TODO - add docstring
        '''
        '''
        surrounding_coordinates = self.get_surrounding_coordinates(x, y)
        acids = []
        for cor in surrounding_coordinates:
            try:
                acid = self.positions[cor]
                acids.append(acid)
            except KeyError:
                pass

        return acids


    def clear_protein(self):
        '''
        Sets score to zero, clears the positions dictionary and the forbidden folds list for every amino acid.
        '''
        self.score = 0
        
        for amino in self.aminoacids:
            amino.forbidden_folds.clear()
        
        self.positions.clear()


    def get_sorted_positions(self):
        '''
        Returns a list of positions, sorted by index of the amino acids.
        '''
        lst = self.positions.items()
        sorted_by_index = sorted(lst, key=lambda x: x[1].index)

        return sorted_by_index


    def __repr__(self):
        return f"{self.id}: f{self.positions}"