from email.utils import formatdate, make_msgid
from email.mime.multipart import MIMEMultipart
from .headers import date, message_id


class Envelope(object):
    def __init__(self, stamp, enclosure):
        self.stamp = stamp
        self.enclosure = enclosure

    def mime(self):
        mime = MIMEMultipart()
        for item in self.enclosure:
            mime.attach(item.mime())
        return mime

    def info(self):
        return self.stamp.prepare(self.mime())
