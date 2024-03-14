class Peer:
    # 
    def connect(self):
        if self.perform_handshake():
            self.is_valid_peer = True
            self.start_exchanging_messages()
        else:
            self.is_valid_peer = False
        
    def __init__(peer_id, peer_ip, peer_port):
        self.keep_running = True
        pass

    #returns true on success, false otherwise
    def perform_handshake():
        pass

    #if we should not attempt to communicate with this peer, return false
    #think: connection already timed out, 
    def is_valid_peer(self):
        pass

    def start_exchanging_messages():
        while self.keep_running and self.is_valid_peer:
            msg = get_message

    #signals that we need to stop sending messages, kills the thread
    def stop_exchanging_messages():
        pass

