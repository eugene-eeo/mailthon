import mimetypes


def inject_headers(headers, mime):
    for key in headers:
        del mime[key]
        mime[key] = headers[key]


def guess(filename, fallback='application/octet-stream'):
    guessed, encoding = mimetypes.guess_type(filename, strict=False)
    if guessed is None:
        return fallback, encoding
    return guessed, encoding


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


def embed(headers, mime):
    info = Info(mime)
    for item in headers:
        item.update(info)
    info.inject_headers()
    return info
