class Piece:
    pass

class BlockManager:

    #previously downloaded pieces of the data are stored somewhere, load them in
    def get_stored_pieces(self):
        pass

    #maybe this is synonymous with "get_missing_pieces", or somethign that can be named "has missing pieces"
    def finished_downloading(self):
        return False

    def get_piece_length(self):
        return self.piece_length

    def __init__(self, piece_length):
        self.piece_length = piece_length

        #or maybe call this self.pieces?
        self.data = self.get_stored_pieces()

    def add_block(self, block):
        pass

    def get_missing_pieces(self):
        pass
