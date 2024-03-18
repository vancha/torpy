from enum import Enum

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
    #returns a message from a socket
    def from_socket(socket):
        length_prefix = Utils.bytes_to_int(socket.recv(4))
    
    #returns the message_type
    def get_type(self):
        pass

