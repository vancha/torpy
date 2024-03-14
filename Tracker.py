from enum import Enum

class TrackerResponseType(Enum):
    FAIL = 1,
    WARINING = 2,
    SUCCESS = 3,

class TrackerResponse:
    def from_response(tracker_response):
        pass

class Tracker:
    #a dict that must always have a field called type
    def send_tracker_request():
        pass


