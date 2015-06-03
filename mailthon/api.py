"""
    mailthon.api
    ~~~~~~~~~~~~

    Implements simple-to-use wrapper functions over
    the more verbose object-oriented core.

    :copyright: (c) 2015 by Eeo Jun
    :license: MIT, see LICENSE for details.
"""

from mailthon.enclosure import HTML, Attachment
from mailthon.envelope import Envelope
from mailthon.postman import Postman
from mailthon.middleware import TLS, Auth
import mailthon.headers as headers


def email(sender=None, receivers=(), cc=(), bcc=(),
          subject=None, content=None, encoding='utf8',
          attachments=()):
    """
    Creates an Envelope object with a HTML *content*.

    :param content: HTML content.
    :param encoding: Encoding of the email.
    :param attachments: List of filenames to
        attach to the email.
    """
    enclosure = [HTML(content, encoding)]
    enclosure.extend(Attachment(k) for k in attachments)
    return Envelope(
        headers=[
            headers.subject(subject),
            headers.sender(sender),
            headers.to(*receivers),
            headers.cc(*cc),
            headers.bcc(*bcc),
            headers.date(),
            headers.message_id(),
        ],
        enclosure=enclosure,
    )


def postman(host, port=587, auth=(None, None),
            force_tls=False, options=None):
    """
    Creates a Postman object with TLS and Auth
    middleware. TLS is placed before authentication
    because usually authentication happens and is
    accepted only after TLS is enabled.

    :param auth: Tuple of (username, password) to
        be used to ``login`` to the server.
    :param force_tls: Whether TLS should be forced.
    :param options: Dictionary of keyword arguments
        to be used when the SMTP class is called.
    """
    return Postman(
        host=host,
        port=port,
        options=options,
        middlewares=[
            TLS(force=force_tls),
            Auth(*auth),
        ],
    )
