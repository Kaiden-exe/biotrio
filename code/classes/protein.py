from code.classes.aminoacid import AminoAcid
import csv
from operator import itemgetter

class Protein():
    def __init__(self, source, protein_id):
        self.id = protein_id
        self.aminoacids = self.load_proteins(source, protein_id)
        self.score = 0
        # key = (x, y), value = AminoAcid()
        self.positions = {}
        self.depth_index = 0


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
        Converts the string of aminoacids into a list of chars,
        then returns a list of aminoacids accordingly.
        '''
        # protein = lijst van chars H/P/C
        protein = []
        protein[:0] = aminos
        acidlist = []
        index = 0
        for acid_id in protein:
            amino = AminoAcid(acid_id, index)
            acidlist.append(amino)
            index += 1
        return acidlist


    def add_position(self, acid, x, y):
        '''
        Add the coordinates of a specific aminoacid to positions dictionary.
        '''
        self.positions[(x, y)] = acid


    def set_stability(self):
        '''
        Analyses folded protein for H/H or H/C bonds and returns stability.
        '''
        coordinates = self.positions.keys()
        stability = 0
        for x, y in coordinates:
            acid = self.positions[(x, y)]
            if acid.id == 'H' or acid.id == 'C':
                surrounding = self.get_surrounding_coordinates(x, y)
                surrounding_aminos = []
                for coordinate in surrounding:
                    try:
                        amino = self.positions[coordinate]
                        surrounding_aminos.append(amino)
                    except KeyError:
                        pass
                            
                for surround in surrounding_aminos:
                    if surround.index > acid.index + 1:
                        if surround.id == 'C' and acid.id == 'C':
                            stability -= 5
                        elif acid.id == 'H' and surround.id == 'H':
                            stability -= 1
                        elif acid.id == 'C' and surround.id == 'H':
                            stability -= 1
                        elif acid.id == 'H' and surround.id == 'C':
                            stability -= 1
        # stability /= 2
        self.score = stability

    def remove_last(self):
        '''
        Removes the acid with the highest index number from positions
        and adds the folding of the second to last acid to a list of forbidden folds.
        Returns the coordinates of the second to last aminoacid.
        '''
        # Create a list, sorted by index and take the highest
        lst = self.positions.items()
        sorted_by_index = sorted(lst, key=lambda x: x[1].index)
        last = sorted_by_index.pop()

        # Delete last added acid from positions
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
        return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


    def clear_protein(self):
        '''
        Sets score to zero and clears the positions dictionary
        '''
        self.score = 0
        self.positions.clear()


    def get_sorted_positions(self):
        '''
        Returns a list of positions, sorted by index of the aminoacids
        '''
        lst = self.positions.items()
        sorted_by_index = sorted(lst, key=lambda x: x[1].index)
        return sorted_by_index


    def __repr__(self):
        return f"{self.id}: {self.aminoacids}: {self.positions}"