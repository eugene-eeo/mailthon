class Response:
    def __init__(self, status, message, rejected):
        self.status_code = status
        self.message = message
        self.rejected = {}
        for key, pair in rejected.items():
            self.rejected[key] = self.from_pair(pair)

    @classmethod
    def from_pair(cls, pair, rejected={}):
        status, message = pair
        return cls(status, message, rejected)

    @property
    def ok(self):
        return self.status_code == 250 and not self.rejected
