from email.encoders import encode_base64, encode_noop
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.utils import quote
from os.path import basename
import mimetypes


class Attachment(object):
    def __init__(self, headers=None):
        self.headers = headers or {}

    def inject_headers(self, mime):
        for key, value in self.headers.items():
            mime[key] = value

    def prepare_mime(self):
        raise NotImplementedError

    def mime(self):
        mime = self.prepare_mime()
        self.inject_headers(mime)
        return mime


class PlainText(Attachment):
    filetype = 'plain'

    def __init__(self, content, encoding='utf-8', **kwargs):
        Attachment.__init__(self, **kwargs)
        self.content = content
        self.encoding = encoding

    def prepare_mime(self):
        return MIMEText(self.content,
                        self.filetype,
                        self.encoding)


class HTML(PlainText):
    filetype = 'html'


class Image(Attachment):
    def __init__(self, content, mimetype=None, **kwargs):
        Attachment.__init__(self, **kwargs)
        self.content = content
        self.mimetype = mimetype

    def prepare_mime(self):
        return MIMEImage(self.content,
                         self.mimetype)


def guess_mimetype(filename, fallback):
    guessed, encoding = mimetypes.guess_type(filename, strict=False)
    if guessed is None:
        return fallback, encoding
    return guessed, encoding


class Raw(Attachment):
    def __init__(self, content, mimetype, encoding=None,
                 encoder=encode_noop, **kwargs):
        Attachment.__init__(self, **kwargs)
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
    def from_filename(cls, path, fallback='text/plain'):
        filename = basename(path)
        mimetype, encoding = guess_mimetype(filename, fallback)

        encoder = encode_base64 if mimetype != 'text/plain' else encode_noop
        disposition = 'attachment; filename="%s"' % quote(filename)

        with open(path, 'rb') as handle:
            return cls(
                content=handle.read(),
                mimetype=mimetype,
                encoding=encoding,
                encoder=encoder,
                headers={'Content-Disposition': disposition},
                )
