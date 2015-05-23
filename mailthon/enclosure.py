from email.encoders import encode_base64, encode_noop
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from os.path import basename
from .helpers import inject_headers, guess
from .headers import ContentDisposition


class Enclosure(object):
    def __init__(self, headers=()):
        self.headers = dict(headers)

    def inject_headers(self, mime):
        inject_headers(self.headers, mime)

    def prepare_mime(self):
        raise NotImplementedError

    def mime(self):
        mime = self.prepare_mime()
        self.inject_headers(mime)
        return mime


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


class Image(Enclosure):
    def __init__(self, content, mimetype=None, **kwargs):
        Enclosure.__init__(self, **kwargs)
        self.content = content
        self.mimetype = mimetype

    def prepare_mime(self):
        return MIMEImage(self.content,
                         self.mimetype)


class Raw(Enclosure):
    def __init__(self, content, mimetype, encoding=None,
                 encoder=encode_noop, **kwargs):
        Enclosure.__init__(self, **kwargs)
        self.content = content
        self.mimetype = mimetype
        self.encoding = encoding
        self.encoder = encoder

    def prepare_mime(self):
        mime = MIMEBase(*self.mimetype.split('/'))
        mime.set_payload(self.content)
        mime['Content-Encoding'] = self.encoding
        self.encoder(mime)
        return mime

    @classmethod
    def from_filename(cls, path, default='application/octet-stream'):
        filename = basename(path)
        mimetype, encoding = guess(filename, default)

        encoder = encode_base64 if mimetype != 'text/plain' else encode_noop
        headers = [
            ContentDisposition('attachment', filename)
        ]

        with open(path, 'rb') as handle:
            return cls(
                content=handle.read(),
                mimetype=mimetype,
                encoding=encoding,
                encoder=encoder,
                headers=headers,
                )
