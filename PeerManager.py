from BlockManager import BlockManager
from Peer import Peer
from Tracker import Tracker

class PeerManager:
    '''
    can generate peer connections based on the tracker response. Knows which blocks to requests because of access to the block manager.
    '''
    def __init__(self, tracker_response, parsed_metainfo_file):
        self.block_manager = BlockManager(parsed_metainfo_file)
        self.peer_list = [Peer(peer[b'ip'].decode('utf-8'), peer[b'peer id'], peer[b'port'], parsed_metainfo_file ) for peer in tracker_response[b'peers']]

    def has_active_peers(self):
        for peer in self.peer_list:
            if peer.is_active:
                return True
        return False

    def request_more_peers(self):
        #if we are not exceeding the maximum number of requests within a timespan for our tracker, request more peers
        pass

    def update(self):
        #probably does something like check if there's active connections. Request more peers if not.
        pass        

