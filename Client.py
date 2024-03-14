class Client:
    #parses the metainfo file, returns the bdecoded results with all values as a dictionary
    def parse_metainfo_file(file):
        pass

    def __init__(metainfo_file, peer_id):
        self.parsed_metainfo_file = self.parse_metainfo_file(metainfo_file)
        self.tracker_response = self.self.send_tracker_request()

        #if we got an actual peer list(with a sucessful tracker response), start the peer wire protocol
        if self.tracker_response.type == TrackerResponseType.SUCCESS:
            self.start_peer_wire_protocol()

    #gets peers from self.tracker_response, opens a thread for each of them with a call to peer.connect
    def start_peer_wire_protocol(self):
        pass

