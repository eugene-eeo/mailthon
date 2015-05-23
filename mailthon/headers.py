from email.utils import quote


class Header(object):
    key = None

    def __init__(self, value):
        self.value = value

    def __iter__(self):
        yield self.key
        yield self.value


class MultiHeader(Header):
    def __init__(self, *values):
        self.value = ', '.join(values)


class Cc(MultiHeader):
    key = 'Cc'


class Bcc(MultiHeader):
    key = 'Bcc'


class ContentID(Header):
    key = 'Content-ID'

    def __init__(self, value):
        self.value = '<%s>' % value


class ContentDisposition(Header):
    key = 'Content-Disposition'

    def __init__(self, disposition, filename):
        self.value = '%s; filename="%s"' % (disposition, quote(filename))
