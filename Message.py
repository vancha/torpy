from enum import Enum

class MessageType(Enum):
    KEEPALIVE = (),
    CHOKE = (),
    UNCHOKE = (),
    INTERESTED = (),
    NOT_INTERESTED = (),
    HAVE = (),
    BITFIELD = (),
    REQUEST = (),
    PIECE = (),
    CANCEL = (),
    PORT = ()

class Message(Enum):
    #returns a message from a socket
    def from_socket(socket):
        length_prefix = Utils.bytes_to_int(socket.recv(4))

