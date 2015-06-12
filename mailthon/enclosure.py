"""
    mailthon.enclosure
    ~~~~~~~~~~~~~~~~~~

    Implements Enclosure objects.

    :copyright: (c) 2015 by Eeo Jun
    :license: MIT, see LICENSE for details.
"""

from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename

from .headers import Headers, content_disposition
from .helpers import guess


class Enclosure(object):
    """
    Base class for Enclosure objects to inherit from.
    An enclosure can be sent on it's own or wrapped
    inside an Envelope object.

    :param headers: Iterable of headers to include.
    """

    def __init__(self, headers=()):
        self.headers = Headers(headers)
        self.content = None

    @property
    def sender(self):
        """
        Returns the sender of the enclosure, obtained
        from the headers.
        """
        return self.headers.sender

    @property
    def receivers(self):
        """
        Returns a list of receiver addresses.
        """
        return self.headers.receivers

    def mime_object(self):
        """
        To be overriden. Returns the generated MIME
        object, without applying the internal headers.
        """
        raise NotImplementedError

    def mime(self):
        """
        Returns the finalised mime object, after
        applying the internal headers. Usually this
        is not to be overriden.
        """
        mime = self.mime_object()
        self.headers.prepare(mime)
        return mime

    def string(self):
        """
        Returns the stringified MIME object, ready
        to be sent via sendmail.
        """
        return self.mime().as_string()


class Collection(Enclosure):
    """
    Multipart enclosure that allows the inclusion of
    multiple enclosures into one single object. Note
    that :class:`~mailthon.enclosure.Collection`
    objects can be nested inside one another.

    :param *enclosures: pass in any number of
        enclosure objects.
    :param subtype: Defaults to ``mixed``, the
        multipart subtype.
    :param headers: Optional headers.
    """

    def __init__(self, *enclosures, **kwargs):
        self.subtype = kwargs.pop('subtype', 'mixed')
        self.enclosures = enclosures
        Enclosure.__init__(self, **kwargs)

    def mime_object(self):
        mime = MIMEMultipart(self.subtype)
        for item in self.enclosures:
            mime.attach(item.mime())
        return mime


class PlainText(Enclosure):
    """
    Enclosure that has a text/plain mimetype.

    :param content: Unicode or bytes string.
    :param encoding: Encoding used to serialize the
        content or the encoding of the content.
    :param headers: Optional headers.
    """

    subtype = 'plain'

    def __init__(self, content, encoding='utf-8', **kwargs):
        Enclosure.__init__(self, **kwargs)
        self.content = content
        self.encoding = encoding

    def mime_object(self):
        return MIMEText(self.content,
                        self.subtype,
                        self.encoding)


class HTML(PlainText):
    """
    Subclass of PlainText with a text/html mimetype.
    """

    subtype = 'html'


class Binary(Enclosure):
    """
    An Enclosure subclass for binary content. If the
    content is HTML or any kind of plain-text then
    the HTML or PlainText Enclosures are receommended
    since they have a simpler interface.

    :param content: A bytes string.
    :param mimetype: Mimetype of the content.
    :param encoding: Optional encoding of the content.
    :param encoder: An optional encoder_ function.
    :param headers: Optional headers.

    .. _encoder: https://docs.python.org/2/library/email.encoders.html
    """

    def __init__(self, content, mimetype, encoding=None,
                 encoder=encode_base64, **kwargs):
        Enclosure.__init__(self, **kwargs)
        self.content = content
        self.mimetype = mimetype
        self.encoding = encoding
        self.encoder = encoder

    def mime_object(self):
        mime = MIMEBase(*self.mimetype.split('/'))
        mime.set_payload(self.content)
        if self.encoding:
            del mime['Content-Type']
            mime.add_header('Content-Type',
                            self.mimetype,
                            charset=self.encoding)
        self.encoder(mime)
        return mime


class Attachment(Binary):
    """
    Binary subclass for easier file attachments.
    The advantage over directly using the Binary
    class is that the Content-Disposition header
    is automatically set, the mimetype guessed,
    and the content lazily returned.

    :param path: Absolute/Relative path to the file.
    :param headers: Optional headers.
    """

    def __init__(self, path, headers=()):
        self.path = path
        self.mimetype, self.encoding = guess(path)
        self.encoder = encode_base64
        heads = dict([content_disposition('attachment', basename(path))])
        heads.update(headers)
        self.headers = Headers(heads)

    @property
    def content(self):
        """
        Lazily returns the bytes contents of the file.
        """
        with open(self.path, 'rb') as handle:
            return handle.read()
