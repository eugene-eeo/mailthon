from email.utils import formatdate, make_msgid
from email.mime.multipart import MIMEMultipart
from .helpers import embed


class Envelope(object):
    def __init__(self, headers, enclosure):
        self.headers = headers
        self.enclosure = enclosure

    def mime(self):
        mime = MIMEMultipart()
        for item in self.enclosure:
            mime.attach(item.mime())
        return mime

    def info(self):
        return embed(self.headers, self.mime())
