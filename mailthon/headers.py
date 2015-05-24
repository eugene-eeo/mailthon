from email.utils import quote, formatdate, make_msgid


def cc(*values):
    yield 'Cc'
    yield ', '.join(values)


def bcc(*values):
    yield 'Bcc'
    yield ', '.join(values)


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
