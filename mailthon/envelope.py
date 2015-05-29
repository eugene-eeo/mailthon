"""
    mailthon.envelope
    ~~~~~~~~~~~~~~~~~

    Implements the Envelope object.

    :copyright: (c) 2015 by Eeo Jun
    :license: MIT, see LICENSE for details.
"""

from email.mime.multipart import MIMEMultipart
from .headers import Headers


class Envelope(object):
    """
    Encapsulates the concept of an Envelope- there
    can be multiple stamps (*headers*) and multiple
    "things" inside the *enclosure*.

    :param headers: An iterable/mapping of headers.
    :param enclosure: A list of enclosure objects.
    """

    def __init__(self, headers, enclosure, mail_from=None):
        self.headers = Headers(headers)
        self.enclosure = enclosure
        self.mail_from = mail_from

    @property
    def sender(self):
        """
        Returns the sender of the envelope, obtained
        from the headers.
        """
        return self.headers.sender

    @property
    def mail_from(self):
        """
        Dictates the sender argument being passed to
        the SMTP.sendmail method. This is different
        from the ``sender`` property as it is the
        *real* sender, but the ``sender`` property
        is merely what *appears* on the email. If it
        is not set, the real sender is then inferred
        from the headers.
        """
        return self._mail_from or self.sender

    @mail_from.setter
    def mail_from(self, value):
        self._mail_from = value

    @property
    def receivers(self):
        """
        Returns a list of receiver addresses.
        """
        return self.headers.receivers

    def mime(self):
        """
        Returns a mime object. Internally this
        generates a ``MIMEMultipart`` object,
        attaches the enclosures, then prepares
        it using the internal headers object.
        """
        mime = MIMEMultipart()
        for item in self.enclosure:
            mime.attach(item.mime())
        self.headers.prepare(mime)
        return mime

    def string(self):
        """
        Returns the MIME object as a string-
        i.e., calls the ``as_string`` method of
        the generated MIME object.
        """
        return self.mime().as_string()
