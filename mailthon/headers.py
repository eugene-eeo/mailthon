from email.utils import quote, formatdate, make_msgid


class Header(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def update(self, info):
        info.headers[self.key] = self.value


class HeaderTemplate(Header):
    key = None

    def __init__(self, value):
        self.value = value


class MultiHeader(HeaderTemplate):
    def __init__(self, *values):
        self.values = values
        self.value = ', '.join(values)


class From(HeaderTemplate):
    key = 'From'

    def update(self, info):
        info.headers[self.key] = self.value
        info.sender = self.value


class To(MultiHeader):
    key = 'To'

    def update(self, info):
        info.headers[self.key] = self.value
        info.receivers.extend(self.values)


class Subject(HeaderTemplate):
    key = 'Subject'


class Cc(To):
    key = 'Cc'


class Bcc(Header):
    key = 'Bcc'

    def __init__(self, *values):
        self.values = values

    def update(self, info):
        info.receivers.extend(self.values)


class ContentDisposition(Header):
    key = 'Content-Disposition'

    def __init__(self, disposition, filename):
        self.value = '%s; filename="%s"' % (disposition, quote(filename))


class Date(Header):
    key = 'Date'

    def __init__(self, time=None):
        self.time = time

    @property
    def value(self):
        return self.time or formatdate(localtime=True)


class MessageID(Header):
    key = 'Message-ID'

    def __init__(self, string=None, idstring=None):
        self.value = string or make_msgid(idstring)
