from email.mime.multipart import MIMEMultipart
from .headers import Headers


class Envelope(object):
    def __init__(self, headers, enclosure):
        self.headers = Headers(headers)
        self.enclosure = enclosure

    @property
    def sender(self):
        return self.headers.sender

    @property
    def receivers(self):
        return self.headers.receivers

    def mime(self):
        mime = MIMEMultipart()
        for item in self.enclosure:
            mime.attach(item.mime())
        self.headers.prepare(mime)
        return mime

    def string(self):
        return self.mime().as_string()
