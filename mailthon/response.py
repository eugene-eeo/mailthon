class Response:
    def __init__(self, pair):
        status, message = pair
        self.status_code = status
        self.message = message

    @property
    def ok(self):
        return self.status_code == 250


class Rejected(Response):
    def __init__(self, pair, receipeint):
        Response.__init__(self, pair)
        self.receipient = receipient


class SendmailResponse(Response):
    def __init__(self, pair, rejected):
        Response.__init__(self, pair)
        self.rejected = [
            Rejected(pair, addr) for addr, pair in rejected.items()
        ]

    @property
    def ok(self):
        return Response.ok.fget(self) and not self.rejected
