class Info(object):
    def __init__(self, mime):
        self.mime = mime
        self.sender = None
        self.receivers = []
        self.headers = {}

    def inject_headers(self):
        inject_headers(self.headers, self.mime)

    def string(self):
        return self.mime.as_string()
