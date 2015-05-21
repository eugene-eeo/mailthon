class Response:
    def __init__(self, status, message):
        self.status_code = status
        self.message = message

    @property
    def ok(self):
        return self.status_code == 250
