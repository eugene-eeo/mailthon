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

    def __init__(self, headers, enclosure):
        self.headers = Headers(headers)
        self.enclosure = enclosure

    @property
    def sender(self):
        """
        Returns the sender of the envelope, obtained
        from the headers.
        """
        return self.headers.sender

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
