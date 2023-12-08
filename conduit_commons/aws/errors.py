class MissingRequiredParams(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Missing a required paramaters"
        super().__init__(msg, *args, **kwargs)
