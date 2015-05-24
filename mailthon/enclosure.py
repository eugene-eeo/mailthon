from email.encoders import encode_base64, encode_noop
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from os.path import basename
from .helpers import inject_headers, guess
from .headers import ContentDisposition, Header
from .stamp import Stamp


class Enclosure(object):
    def __init__(self, headers=()):
        self.stamp = Stamp(headers)

    def prepare_mime(self):
        raise NotImplementedError

    def mime(self):
        mime = self.prepare_mime()
        info = self.stamp.prepare(mime)
        return info.mime


class PlainText(Enclosure):
    subtype = 'plain'

    def __init__(self, content, encoding='utf-8', **kwargs):
        Enclosure.__init__(self, **kwargs)
        self.content = content
        self.encoding = encoding

    def prepare_mime(self):
        return MIMEText(self.content,
                        self.subtype,
                        self.encoding)


class HTML(PlainText):
    subtype = 'html'


class Binary(Enclosure):
    def __init__(self, content, mimetype, encoding=None,
                 encoder=encode_base64, **kwargs):
        Enclosure.__init__(self, **kwargs)
        self.content = content
        self.mimetype = mimetype
        self.encoding = encoding
        self.encoder = encoder

    def prepare_mime(self):
        mime = MIMEBase(*self.mimetype.split('/'))
        mime.set_payload(self.content)
        if self.encoding:
            del mime['Content-Type']
            mime.add_header('Content-Type',
                            self.mimetype,
                            charset=self.encoding)
        self.encoder(mime)
        return mime


class Attachment(Binary):
    def __init__(self, path, headers=()):
        self.path = path
        self.mimetype, self.encoding = guess(path)
        self.encoder = encode_base64
        heads = [
            ContentDisposition('attachment', basename(path))
        ]
        heads.extend(headers)
        self.stamp = Stamp(heads)

    @property
    def content(self):
        with open(self.path, 'rb') as handle:
            return handle.read()
