from email.mime.text import MIMEText


class Attachment(object):
    def __init__(self, content):
        self.content = content

    def mime(self):
        pass


class PlainText(Attachment):
    def __init__(self, content, encoding='utf-8'):
        Attachment.__init__(self, content)
        self.encoding = encoding

    def mime(self):
        return MIMEText(self.content,
                        'plain',
                        self.encoding)


class HTML(PlainText):
    def mime(self):
        return MIMEText(self.content,
                        'html',
                        self.encoding)
