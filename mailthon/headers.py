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


def content_id(filename):
    yield 'Content-ID'
    yield '<%s>' % filename


def content_disposition(disposition, filename):
    yield 'Content-Disposition'
    yield '%s; filename="%s"' % (disposition, quote(filename))


def date(time=None):
    yield 'Date'
    yield time or formatdate(localtime=True)


def message_id(string=None, idstring=None):
    yield 'Message-ID'
    yield string or make_msgid(idstring)
