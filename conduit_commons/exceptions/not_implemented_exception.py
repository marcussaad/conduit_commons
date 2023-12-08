class EventNotImplemented(Exception):
    def __init__(self, message="Event not implemented"):
        super().__init__(message)
