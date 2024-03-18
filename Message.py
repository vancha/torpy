from enum import Enum

'''
Represents a message in the bittorrent protocol. The messagetype lists all the possible types of messages there are.
'''

class MessageType(Enum):
    KEEPALIVE = 1,
    CHOKE = 2,
    UNCHOKE = 3,
    INTERESTED = 4,
    NOT_INTERESTED = 5,
    HAVE = 6,
    BITFIELD = 7,
    REQUEST = 8,
    PIECE = 9,
    CANCEL = 10,
    PORT = 11

class Message(Enum):
    #builds a message from a socket connection. Blocks until a message has been received
    def __init__(self, socket):
        #get length prefix
        length_prefix = Utils.bytes_to_int(socket.recv(4))
        #
    
    #returns the message_type
    def get_type(self):
        return self.type

