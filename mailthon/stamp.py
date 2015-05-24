from .helpers import inject_headers


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


class Stamp(object):
    def __init__(self, headers=()):
        self.headers = headers

    def prepare(self, mime):
        info = Info(mime)
        for item in self.headers:
            item.update(info)
        info.inject_headers()
        return info
