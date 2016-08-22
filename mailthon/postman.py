"""
    mailthon.postman
    ~~~~~~~~~~~~~~~~

    This module implements the central Postman object.

    :copyright: (c) 2015 by Eeo Jun
    :license: MIT, see LICENSE for details.
"""

from contextlib import contextmanager
from smtplib import SMTP
from .response import SendmailResponse
from .helpers import stringify_address


class Session(object):
    """
    Represents a connection to some server or external
    service, e.g. some REST API. The underlying transport
    defaults to SMTP but can be subclassed.

    :param **kwargs: Keyword arguments to be passed to
        the underlying transport.
    """

    def __init__(self, **kwargs):
        self.conn = SMTP(**kwargs)
        self.conn.ehlo()

    def teardown(self):
        """
        Tear down the connection.
        """
        self.conn.quit()

    def send(self, envelope):
        """
        Send an *envelope* which may be an envelope
        or an enclosure-like object, see
        :class:`~mailthon.enclosure.Enclosure` and
        :class:`~mailthon.envelope.Envelope`, and
        returns a :class:`~mailthon.response.SendmailResponse`
        object.
        """
        rejected = self.conn.sendmail(
            stringify_address(envelope.sender),
            [stringify_address(k) for k in envelope.receivers],
            envelope.string(),
        )
        status_code, reason = self.conn.noop()
        return SendmailResponse(
            status_code,
            reason,
            rejected,
        )


class Postman(object):
    """
    Encapsulates a connection to a server, created by
    some *session* class and provides middleware
    management and setup/teardown goodness. Basically
    is a layer of indirection over session objects,
    allowing for pluggable transports.

    :param session: Session class to be used.
    :param middleware: Middlewares to use.
    :param **kwargs: Options to pass to session class.
    """

    def __init__(self, session=Session, middlewares=(), **options):
        self.session = session
        self.options = options
        self.middlewares = list(middlewares)

    def use(self, middleware):
        """
        Use a certain callable *middleware*, i.e.
        append it to the list of middlewares, and
        return it so it can be used as a decorator.
        """
        self.middlewares.append(middleware)
        return middleware

    @contextmanager
    def connection(self):
        """
        A context manager that returns a connection
        to the server using some *session*.
        """
        conn = self.session(**self.options)
        try:
            for item in self.middlewares:
                item(conn)
            yield conn
        finally:
            conn.teardown()

    def send(self, envelope):
        """
        Sends an *enclosure* and return a response
        object.
        """
        with self.connection() as conn:
            return conn.send(envelope)
