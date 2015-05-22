from email.encoders import encode_base64, encode_noop
from email.utils import quote
import mimetypes
from os.path import basename
from .builder import MIMEBase, MIMEImage, MIMEText


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


def get_mimetype(filename, fallback):
    guessed = mimetypes.guess_type(filename, False)[0]
    if guessed is None:
        return fallback
    return guessed


class Raw(Attachment):
    def __init__(self, content, mimetype, encoding=None, encoder=encode_noop, **kwargs):
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
    def from_filename(cls, path, encoding=None, fallback='text/plain'):
        filename = basename(path)
        mimetype = get_mimetype(filename, fallback)

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
