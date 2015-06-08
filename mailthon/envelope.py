"""
    mailthon.envelope
    ~~~~~~~~~~~~~~~~~

    Implements the Envelope object.

    :copyright: (c) 2015 by Eeo Jun
    :license: MIT, see LICENSE for details.
"""


class Envelope(object):
    """
    Enclosure adapter for encapsulating the concept of
    an Envelope- a wrapper around some content in the
    form of an *enclosure*, and dealing with SMTP
    specific idiosyncracies.

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
        """
        Returns the real sender if set in the *mail_from*
        parameter/attribute, else returns the sender
        attribute from the wrapped enclosure.
        """
        return self.mail_from or self.enclosure.sender

    @property
    def receivers(self):
        """
        Returns the "real" receivers which will be passed
        to the ``RCPT TO`` command (in SMTP) if specified
        in the *rcpt_to* attribute/parameter. Else, return
        the receivers attribute from the wrapped enclosure.
        """
        return self.rcpt_to or self.enclosure.receivers

    def mime(self):
        """
        Returns the mime object from the enclosure.
        """
        return self.enclosure.mime()

    def string(self):
        """
        Returns the stringified mime object.
        """
        return self.enclosure.string()
