from email.utils import quote, formatdate, make_msgid, getaddresses


class Headers(dict):
    @property
    def resent(self):
        return 'Resent-Date' in self

    @property
    def sender(self):
        to_fetch = (
            ['Resent-Sender', 'Resent-From'] if self.resent else
            ['Sender', 'From']
        )
        for item in to_fetch:
            if item in self:
                return self[item]

    @property
    def receivers(self):
        attrs = (
            ['Resent-To', 'Resent-Cc', 'Resent-Bcc'] if self.resent else
            ['To', 'Cc', 'Bcc']
        )
        addrs = (f for f in (self.get(item, []) for item in attrs) if f)
        return [a[1] for a in getaddresses(addrs)]

    def prepare(self, mime):
        for key in self:
            if key == 'Bcc' or key == 'Resent-Bcc':
                continue
            del mime[key]
            mime[key] = self[key]


def subject(text):
    yield 'Subject'
    yield text


def sender(address):
    yield 'Sender'
    yield address


def to(*addrs):
    yield 'To'
    yield ', '.join(addrs)


def cc(*addrs):
    yield 'Cc'
    yield ', '.join(addrs)


def bcc(*addrs):
    yield 'Bcc'
    yield ', '.join(addrs)


def content_disposition(disposition, filename):
    yield 'Content-Disposition'
    yield '%s; filename="%s"' % (disposition, quote(filename))


def date(time=None):
    yield 'Date'
    yield time or formatdate(localtime=True)


def message_id(string=None, idstring=None):
    yield 'Message-ID'
    yield string or make_msgid(idstring)
