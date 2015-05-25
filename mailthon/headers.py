from email.utils import quote, formatdate, make_msgid, getaddresses


class Headers(dict):
    """
    RFC 2822 compliant subclass of a dictionary.
    """

    @property
    def resent(self):
        """
        Tells whether the email was resent, i.e. whether
        the ``Resent-Date`` header was set.
        """
        return 'Resent-Date' in self

    @property
    def sender(self):
        """
        Returns the sender, respecting the Resent-* headers.
        In any case, prefer``Sender`` over ``From``, meaning
        that if ``Sender`` is present then ``From`` is
        ignored, as per the RFC.
        """
        to_fetch = (
            ['Resent-Sender', 'Resent-From'] if self.resent else
            ['Sender', 'From']
        )
        for item in to_fetch:
            if item in self:
                return self[item]

    @property
    def receivers(self):
        """
        Returns a list of receivers, obtained from the To,
        Cc, and Bcc headers, respecting the Resent-*
        headers if the email was resent.
        """
        attrs = (
            ['Resent-To', 'Resent-Cc', 'Resent-Bcc'] if self.resent else
            ['To', 'Cc', 'Bcc']
        )
        addrs = (f for f in (self.get(item) for item in attrs) if f)
        return [a[1] for a in getaddresses(addrs)]

    def prepare(self, mime):
        """
        Preprares a MIME object by applying the headers to
        the other object. Ignores any Bcc or Resent-Bcc
        headers as these are not meant to be set.
        """
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
