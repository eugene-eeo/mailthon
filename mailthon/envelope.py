from email.mime.multipart import MIMEMultipart


class Stamp(object):
    def __init__(self, subject, sender, receivers):
        self.subject = subject
        self.sender = sender
        self.receivers = receivers

    @property
    def receiver_string(self):
        return ', '.join(self.receivers)

    def prepare(self, mime):
        mime['Subject'] = self.subject
        mime['From'] = self.sender
        mime['To'] = self.receiver_string


class Envelope(object):
    def __init__(self, stamp, attachments, headers={}):
        self.stamp = stamp
        self.attachments = attachments
        self.headers = headers.copy()

        self.sender = self.stamp.sender
        self.receivers = self.stamp.receivers

    def put_headers(self, mime):
        for key, value in self.headers.items():
            mime[key] = value

    def prepare(self):
        mime = MIMEMultipart()
        self.stamp.prepare(mime)
        self.put_headers(mime)

        for item in self.attachments:
            mime.attach(item.mime())

        return mime

    def to_string(self):
        return self.prepare().as_string()
