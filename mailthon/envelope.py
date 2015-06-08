"""
    mailthon.envelope
    ~~~~~~~~~~~~~~~~~

    Implements the Envelope object.

    :copyright: (c) 2015 by Eeo Jun
    :license: MIT, see LICENSE for details.
"""


class Envelope(object):
    """
    Encapsulates the concept of an Envelope- there
    can be multiple stamps (*headers*) and multiple
    "things" inside the *enclosure*.

    :param enclosure: An enclosure object to wrap around.
    :param mail_from: The "real" sender. May be omitted.
    :param rcpt_to: A list of "real" email addresses.
        May be omitted.
    """

    def __init__(self, enclosure, mail_from=None, rcpt_to=None):
        self.enclosure = enclosure
        self.mail_from = mail_from
        self.rcpt_to = rcpt_to

    @property
    def sender(self):
        return self.mail_from or self.enclosure.sender

    @property
    def receivers(self):
        return self.rcpt_to or self.enclosure.receivers

    def mime(self):
        return self.enclosure.mime()

    def string(self):
        return self.enclosure.string()
