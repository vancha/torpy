#expects four bytes big endian value
def bytes_to_int(value):
    return int.from_bytes(value, 'big')

#a dict that must always have a field called type
def send_tracker_request():
    pass
