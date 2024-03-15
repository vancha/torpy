from BlockManager import BlockManager

class PeerManager:
    '''
    can generate peer connections based on the tracker response. Knows which blocks to requests because of access to the block manager.
    '''
    def __init__(self, tracker_response, piece_length):
        self.block_manager = BlockManager(piece_length)
        self.peer_list = [peer for peer in tracker_response[b'peers']]

    def has_active_peers(self):
        print(f'currently active peers: {self.peer_list}')
        return True

    def request_more_peers(self):
        #if we are not exceeding the maximum number of requests within a timespan for our tracker, request more peers
        pass

    def update(self):
        #probably does something like check if there's active connections. Request more peers if not.
        pass        

