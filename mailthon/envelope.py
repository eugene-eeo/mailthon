from email.utils import formatdate, make_msgid
from email.mime.multipart import MIMEMultipart
from .headers import date, message_id
from .stamp import Stamp


class Envelope(object):
    def __init__(self, headers, enclosure):
        self.stamp = Stamp(headers)
        self.enclosure = enclosure

    def mime(self):
        mime = MIMEMultipart()
        for item in self.enclosure:
            mime.attach(item.mime())
        return mime

    def info(self):
        return self.stamp.prepare(self.mime())
