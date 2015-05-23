from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from .helpers import inject_headers


class Stamp(object):
    def __init__(self, sender, receivers, subject=None, headers=()):
        self.sender = sender
        self.receivers = receivers
        self.subject = subject
        self.headers = dict(headers)

    @property
    def receiver_string(self):
        return ', '.join(self.receivers)

    def prepare(self, mime):
        headers = {
            'Subject': self.subject,
            'From': self.sender,
            'To': self.receiver_string,
            'Date': formatdate(localtime=True),
        }
        headers.update(self.headers)
        inject_headers(headers, mime)


class Envelope(object):
    def __init__(self, stamp, enclosure):
        self.stamp = stamp
        self.enclosure = enclosure
        self.sender = stamp.sender
        self.receivers = stamp.receivers

    def mime(self):
        mime = MIMEMultipart()
        self.stamp.prepare(mime)

        for item in self.enclosure:
            mime.attach(item.mime())

        return mime

    def to_string(self):
        return self.mime().as_string()
