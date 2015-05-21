import os.path
import mimetypes
from base64 import b64encode
from email.utils import quote
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase


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
    def __init__(self, content, filetype=None, **kwargs):
        Attachment.__init__(self, **kwargs)
        self.content = content
        self.filetype = filetype

    def prepare_mime(self):
        return MIMEImage(self.content,
                         self.filetype)


class Raw(Attachment):
    def __init__(self, mimetype, content, encoding=None, **kwargs):
        Attachment.__init__(self, **kwargs)
        self.major, self.minor = mimetype.split('/', 1)
        self.content = content
        self.encoding = encoding

    def prepare_mime(self):
        mime = MIMEBase(self.major, self.minor)
        mime.set_payload(b64encode(self.content))
        mime['Content-Transfer-Encoding'] = 'base64'
        mime['Content-Encoding'] = self.encoding
        return mime

    @classmethod
    def from_filename(cls, path):
        filetype, encoding = mimetypes.guess_type(path)
        if filetype is None:
            filetype = 'application/octet-stream'

        _, filename = os.path.split(path)
        disposition = 'attachment; filename="%s"' % quote(filename)

        with open(path, 'rb') as handle:
            return Raw(
                mimetype=filetype,
                content=handle.read(),
                encoding=encoding,
                headers={
                    'Content-Disposition': disposition,
                },
            )
