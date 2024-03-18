from Tracker import Tracker
from threading import Thread
import Constants
import socket
import ipaddress
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
        self.is_active      = True
        self.new_pieces     = False
        self.ip             = ipaddress.ip_address(peer_ip)
        self.id             = peer_id
        self.port           = peer_port
        self.info_hash      = Tracker.info_to_info_hash_bytes(parsed_metainfo_file[b'info'])
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
            chars_before_hash   = len(pstrlen)+len(pstr)+len(reserved_bytes)
            their_hash          = response[chars_before_hash : chars_before_hash + len(self.info_hash)]
            if their_hash == self.info_hash:
                print('hashes match! connection started')
            else:
                self.is_active = False
                print('hashes dont match, something fishy going on here. disconnecting')
        except Exception as e:
            print(f'handshake failed for {self.ip}: {e}') 
            return False
            
    def handle_message(self, msg):
        pass
        #get msg type, depending on type, parse it's contents
    
    #an infinite loop, that quits when done or on error. Should add a thread handle to self, so that it can be killed
    def start_exchanging_messages(self):
        print(f'started connection with {self.ip}')
        while self.is_active:
            msg = self.get_message()
            if msg.get_type() == MessageType.PIECE:
                self.new_pieces = True
            self.handle_message(msg)
            
    def has_new_pieces(self):
        return self.new_pieces
        
    #start thread that runs "start_exchanging messages"
    def run(self):
        if self.is_active:
            self.thread_handle = Thread(target=start_exchanging_messages)
            self.thread_handle.run()
        else:
            print('peer not active, not running')
    
    #signals that we need to stop sending messages, kills the thread
    def quit(self):
        if self.is_active:
            self.is_active = False
            self.thread_handle.join()

