from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class Attachment(object):
    def mime(self):
        pass


class PlainText(Attachment):
    filetype = 'plain'

    def __init__(self, content, encoding='utf-8'):
        self.content = content
        self.encoding = encoding

    def mime(self):
        return MIMEText(self.content,
                        self.filetype,
                        self.encoding)


class HTML(PlainText):
    filetype = 'html'


class Image(Attachment):
    def __init__(self, content, filetype=None):
        self.content = content
        self.filetype = filetype

    def mime(self):
        return MIMEImage(self.content,
                         self.filetype)


class Raw(Attachment):
    def __init__(self, mime):
        self.mimeobj = mime

    def mime(self):
        return self.mimeobj
