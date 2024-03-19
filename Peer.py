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
Once the peer receives a block, it will store it, so that it can be retrieved by the peermanager, which will in turn add it to the piecemanager.
'''

class Peer:

    def __del__(self):
        try:
            self.socket.close()
            print(f'closed the socket connection with {self.ip}')
        except:
            print('socket was already closed')
 
    def connect(self):
        print(f'attempting to perform handshake with {self.ip}')
        if self.perform_handshake():
            self.run()
        else:
            self.is_active = False
    
    #file needed to get info hash, which is used for handshake
    def __init__(self, peer_ip, peer_id, peer_port,parsed_metainfo_file):
        self.is_active      = True
        self.new_pieces     = False
        self.has_pieces     = []
        self.finished_blocks= []
        self.ip             = ipaddress.ip_address(peer_ip)
        self.id             = peer_id
        self.port           = peer_port
        self.info_hash      = Tracker.info_to_info_hash_bytes(parsed_metainfo_file[b'info'])
        
        #the mandatory state information to keep track of for peers
        self.peer_choking   = True
        self.peer_interested= False
        self.am_choking     = True
        self.am_interested  = False
        self.connect()
        
    def request_piece(self, piece):
        print(f'requesting piece {piece}')
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
            pass
        elif msg_type == MessageType.CHOKE:
            print('peer choking')
            self.peer_choking = True
        elif msg_type == MessageType.UNCHOKE:
            print('peer unchoked')
            self.peer_choking = False
        elif msg_type == MessageType.INTERESTED:
            print('peer interested')
            self.peer_interested = True
        elif msg_type == MessageType.NOT_INTERESTED:
            print('peer not interested')
            self.peer_interested = False
        elif msg_type == MessageType.HAVE:
            print(f'added piece {msg.payload}')
            #appends the index of the advertised piece to the "has pieces" field, useful for peermanager
            self.has_pieces.append(msg.payload)
        elif msg_type == MessageType.BITFIELD:
            print('received bitfield message')
        elif msg_type == MessageType.REQUEST:
            #ignore for now, we don't advertise having any pieces yet
            pass
        elif msg_type == MessageType.PIECE:
            self.new_pieces = True
            print('received piece yay')
        elif msg_type == MessageType.CANCEL:
            #ignore for now, not useful until later
            pass
        elif msg_type == MessageType.PORT:
            #ignore, also not useful for the time being
            pass
    
    #
    #def has_pieces(self):
    #    return self.has_pieces
    
    #an infinite loop, that quits when done or on error. Should add a thread handle to self, so that it can be killed
    def start_exchanging_messages(self):
        while self.is_active:
            msg = Message.from_socket(self.socket)
            self.handle_message(msg)
            
    def has_new_pieces(self):
        return self.new_pieces
        
    #start thread that runs "start_exchanging messages"
    def run(self):
        if self.is_active:
            self.thread_handle = Thread(target=self.start_exchanging_messages)
            self.thread_handle.start()
        else:
            print('peer not active, not running')
    
    #signals that we need to stop sending messages, kills the thread
    def quit(self):
        if self.is_active:
            print(f'{self.ip} active, stopping')
            self.is_active = False
            self.thread_handle.join()
        else:
            print(f'cannot stop peer because peer not active')

