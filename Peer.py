import Constants
import socket
import ipaddress
from Tracker import Tracker
import urllib.parse

class Peer:
    def __del__(self):
        try:
            self.socket.close()
        except:
            print('socket was already closed')
 
    def connect(self):
        if self.perform_handshake():
            self.start_exchanging_messages()
        self.is_active = False
    
    #file needed to get info hash, which is used for handshake
    def __init__(self, peer_ip, peer_id, peer_port,parsed_metainfo_file):
        self.is_active  = True
        self.ip         = ipaddress.ip_address(peer_ip)
        self.id         = peer_id
        self.port       = peer_port
        self.info_hash  = Tracker.info_to_info_hash_bytes(parsed_metainfo_file[b'info'])
        self.connect()

    #returns true on success, false otherwise. creates self.socket
    def perform_handshake(self):
        pstrlen         = Constants.PSTRLEN
        pstr            = Constants.PSTR
        reserved_bytes  = bytes([0,0,0,0,0,0,0,0])
        request         = pstrlen + pstr + reserved_bytes + self.info_hash + Constants.PEER_ID.encode('utf-8')
        self.socket     = socket.socket(socket.AF_INET, socket.SOCK_STREAM) if self.ip.version == 4 else socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.socket.settimeout(Constants.BITTORRENT_TIMEOUT_SECONDS)
        
        try:
            self.socket.connect((str(self.ip), self.port))
            self.socket.sendall(request)
            response            = self.socket.recv(68)
            print(f'received response: {response}')
            chars_before_hash   = len(pstrlen)+len(pstr)+len(reserved_bytes)
            their_hash          = response[chars_before_hash : chars_before_hash + len(self.info_hash)]
            print(f'their hash: {their_hash}')
            print(f'our hash:   {self.info_hash}')
        except Exception as e:
            print(f'handshake failed for {self.ip}: {e}') 
            return False
        

    #if we should not attempt to communicate with this peer, return false
    #think: connection already timed out, 
    def is_valid_peer(self):
        pass

    #an infinite loop, that quits when done or on error
    def start_exchanging_messages():
        while self.is_active:
            msg = get_message
        print('stopped communicating with peer')

    #signals that we need to stop sending messages, kills the thread
    def stop_exchanging_messages():
        self.is_active = False

