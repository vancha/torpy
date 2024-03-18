from BlockManager import BlockManager
from Peer import Peer
from Tracker import Tracker
import Constants
import time

class PeerManager:
    '''
    can generate peer connections based on the tracker response. Knows which blocks to requests because of access to the block manager.
    '''
    def __init__(self, tracker_response, parsed_metainfo_file):
        self.block_manager = BlockManager(parsed_metainfo_file)
        self.peer_list = [Peer(peer[b'ip'].decode('utf-8'), peer[b'peer id'], peer[b'port'], parsed_metainfo_file ) for peer in tracker_response[b'peers']]
        self.run()
        
        
    def has_active_peers(self):
        for peer in self.peer_list:
            if peer.is_active:
                return True
        return False
    
    def has_inactive_peers(self):
        for peer in self.peer_list:
            if not peer.is_active:
                return True
        return False
    
    def remove_inactive_peers(self):
        for peer in self.peer_list:
            if not peer.is_active:
                peer.quit()
                self.peer_list.remove(peer)
                
    def request_more_peers(self):
        #if we are not exceeding the maximum number of requests within a timespan for our tracker, request more peers
        pass

    def run(self):
        try:
            while True:
                if self.has_inactive_peers():
                    self.remove_inactive_peers()
                if len(self.peer_list)  < Constants.MAX_PEER_CONNECTIONS:
                    self.request_more_peers()
                for peer in self.peer_list:
                    if peer.has_new_pieces():
                        for piece in peer.get_new_piece():
                            self.block_manager.add_piece(piece)
                time.sleep(1)
                
        except KeyboardInterrupt:
            print('keyboard interrupt detected, killing peers')

