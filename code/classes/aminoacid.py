class AminoAcid():
    def __init__(self, acid_id, index):
        self.id = acid_id
        self.folding = None
        self.index = index
        self.forbidden_folds = []

    def __repr__(self):
        return f"{self.id}{self.index}"