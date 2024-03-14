from enum import Enum

import Utils
import Peer
import Message
import Client  
from Tracker import Tracker
        


#Torrent client
class Torpy:
    #parses the metainfo file, returns the bdecoded results with all values as a dictionary
    def parse_metainfo_file(metainfo_file_location):
        pass
    
    def __init__(self, metainfo_file_location, peer_id):
        self.parsed_metainfo_file = Torpy.parse_metainfo_file(metainfo_file_location)
        self.tracker_response = Tracker.send_tracker_request()

        #if we got an actual peer list(with a sucessful tracker response), start the peer wire protocol
        if self.tracker_response.type == TrackerResponseType.SUCCESS:
            self.start_peer_wire_protocol()

    #gets peers from self.tracker_response, opens a thread for each of them with a call to peer.connect
    def start_peer_wire_protocol(self):
        pass

    