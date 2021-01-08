class AminoAcid():
    def __init__(self, id, index):
        # C, P, H
        self.id = id
        # Right, Left, Forward
        self.folding = None
        # Location in protein
        self.index = index

    def __repr__(self):
        return f"{self.id}"