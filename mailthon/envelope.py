from email.utils import formatdate, make_msgid
from email.mime.multipart import MIMEMultipart
from .helpers import inject_headers
from .headers import date, message_id


class Stamp(object):
    def __init__(self, headers=()):
        self.headers = headers

    def prepare(self, info):
        for item in self.headers:
            item.update(info)
        info.inject_headers()


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
        info = Info(self.mime())
        self.stamp.prepare(info)
        return info
