from Tracker import Tracker
from threading import Thread
from Message import Message, MessageType
import Constants
import socket
import ipaddress
import urllib.parse

'''
This represents a peer in the torrent protocol. After a call to connect(), it will attempt to connect with the remote peer it represents, and it will start
a thread that exchanges messages with the peer and this local torrent client.
Once the peer receives a block/piece, it will store it, so that it can be retrieved by the peermanager, which will in turn add it to the blockmanager.
'''

class Peer:
    def __del__(self):
        try:
            self.socket.close()
            print(f'closed the socket connection with {self.ip}')
        except:
            print('socket was already closed')
 
    def connect(self):
        if self.perform_handshake():
            self.run()
        else:
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
            if not their_hash == self.info_hash:
                self.is_active = False
            print(f'connected to {self.ip}')
            return True
        except Exception as e:
            return False
            
    def handle_message(self, msg):
        msg_type = msg.get_type()
        
        if msg_type == MessageType.KEEPALIVE:
            print('received keepalive message')
        elif msg_type == MessageType.CHOKE:
            print('received choke message')
        elif msg_type == MessageType.UNCHOKE:
            print('received unchoke message')
        elif msg_type == MessageType.INTERESTED:
            print('received interested message')
        elif msg_type == MessageType.NOT_INTERESTED:
            print('received not interested message')
        elif msg_type == MessageType.HAVE:
            print('received have message')
        elif msg_type == MessageType.BITFIELD:
            print('received bitfield message')
        elif msg_type == MessageType.REQUEST:
            print('received request message')
        elif msg_type == MessageType.PIECE:
            self.new_pieces = True
            print('received piece yay')
        elif msg_type == MessageType.CANCEL:
            print('received cancel message')
        elif msg_type == MessageType.PORT:
            print('received port message')
    
    #an infinite loop, that quits when done or on error. Should add a thread handle to self, so that it can be killed
    def start_exchanging_messages(self):
        print(f'started connection with {self.ip}')
        while self.is_active:
            msg = Message.from_socket(self.socket)
            self.handle_message(msg)
            
    def has_new_pieces(self):
        return self.new_pieces
        
    #start thread that runs "start_exchanging messages"
    def run(self):
        if self.is_active:
            print(f'{self.ip} active, starting thread')
            self.thread_handle = Thread(target=self.start_exchanging_messages)
            self.thread_handle.run()
            print(f'thread started')
        else:
            print('peer not active, not running')
    
    #signals that we need to stop sending messages, kills the thread
    def quit(self):
        if self.is_active:
            print(f'peer active, stopping')
            self.is_active = False
            self.thread_handle.join()
        else:
            print(f'cannot stop peer because peer not active')

