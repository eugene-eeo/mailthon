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


class Postman(object):
    """
    Encapsulates a connection to a server and knows
    how to send MIME emails over a certain transport.
    When subclassing, change the ``transport`` and
    ``response_cls`` class variables to tweak the
    transport used and the response class, respectively.

    :param host: The address to a server.
    :param port: Port to connect to.
    :param middlewares: An iterable of middleware that
        will be used by the Postman.
    :param options: Dictionary of options to be passed
        to the underlying transport.
    """

    transport = SMTP
    response_cls = SendmailResponse

    def __init__(self, host, port, middlewares=(), options=None):
        self.host = host
        self.port = port
        self.middlewares = list(middlewares)
        self.options = options or {}

    def use(self, middleware):
        """
        Use a certain callable *middleware*, i.e.
        append it to the list of middlewares, and
        return it so it can be used as a decorator.
        Note that the *middleware* is added to the
        end of the middlewares list, so it will be
        called last.
        """
        self.middlewares.append(middleware)
        return middleware

    @contextmanager
    def connection(self):
        """
        A context manager that returns a connection
        to the server using some transport, defaulting
        to SMTP. The transport will be called with
        the server address, port, and options that have
        been passed to the constructor, in that order.
        """
        conn = self.transport(self.host, self.port, **self.options)
        try:
            conn.ehlo()
            for item in self.middlewares:
                item(conn)
            yield conn
        finally:
            conn.quit()

    def deliver(self, conn, envelope):
        """
        Deliver an *envelope* using a given connection
        *conn*, and return the response object. Does
        not close the connection.
        """
        rejected = conn.sendmail(
            stringify_address(envelope.mail_from),
            [stringify_address(k) for k in envelope.receivers],
            envelope.string(),
        )
        return self.response_cls(conn.noop(), rejected)

    def send(self, envelope):
        """
        Sends an *envelope* and return a response
        object.
        """
        with self.connection() as conn:
            return self.deliver(conn, envelope)
