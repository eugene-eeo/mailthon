from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from .attachments import inject_headers


class Stamp(object):
    def __init__(self, subject, sender, receivers, headers=()):
        self.subject = subject
        self.sender = sender
        self.receivers = receivers
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
    def __init__(self, stamp, attachments):
        self.stamp = stamp
        self.attachments = attachments

    @property
    def sender(self):
        return self.stamp.sender

    @property
    def receivers(self):
        return self.stamp.receivers

    def mime(self):
        mime = MIMEMultipart()
        self.stamp.prepare(mime)

        for item in self.attachments:
            mime.attach(item.mime())

        return mime

    def to_string(self):
        return self.mime().as_string()
