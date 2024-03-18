from itertools import batched

class Piece:
    pass

class BlockManager:

    #previously downloaded pieces of the data are stored somewhere, load them in
    def get_stored_pieces(self):
        pass


    def get_piece_length(self):
        return self.piece_length

    def __init__(self, parsed_metainfo_file):#piece_length):
        self.piece_length           = parsed_metainfo_file[b'info'][b'piece length']

        #converts byte hashes to string, those seem more useful
        _pieces                 = parsed_metainfo_file[b'info'][b'pieces']
        _pieces                 = [piece_hash for piece_hash in batched(_pieces, 20)]
        for index, piece_hash in enumerate(_pieces):
            _pieces[index] = ''.join(format(x, '02x') for x in piece_hash)
        self.pieces = _pieces
        self.downloaded_pieces = [False for piece in self.pieces]

        self.outstanding_requests   = []
        self.data = self.get_stored_pieces()

    #def requested(block):
        #update outstanding requests
    #    pass

    def add_block(self, block):
        pass
    
    def add_piece(self, piece):
        pass

    def has_missing_pieces(self):
        return False in self.downloaded_pieces
