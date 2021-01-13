from code.classes.aminoacid import AminoAcid
import csv

class Protein():
    def __init__(self, source, protein_id):
        self.id = protein_id
        self.aminoacids = self.load_proteins(source, protein_id)
        self.score = 0
        # key = (x, y), value = AminoAcid()
        self.positions = {}


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
        Add the coordinates of a specific amino acid to positions dictionary.
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
            if acid.id == 'H':
                surrounding = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                surrounding_aminos = []
                for coordinate in surrounding:
                    try:
                        amino = self.positions[coordinate]
                        surrounding_aminos.append(amino)
                    except KeyError:
                        pass
                            
                for surround in surrounding_aminos:
                    if not surround.index == acid.index + 1 and not surround.index == acid.index - 1:
                        if surround.id == 'H':
                            stability -= 1
                        # if surround.id == 'C':
                        # TODO
        stability /= 2
        self.score = stability


    def __repr__(self):
        return f"{self.id}: f{self.aminoacids}"

