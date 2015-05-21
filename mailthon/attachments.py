from email.mime.text import MIMEText
from email.mime.image import MIMEImage


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
    def __init__(self, mime):
        self.mimeobj = mime

    def mime(self):
        return self.mimeobj
