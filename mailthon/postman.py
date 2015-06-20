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
from .helpers import encode_address


class Session(object):
    def __init__(self, **kwargs):
        self.conn = SMTP(**kwargs)

    def setup(self):
        self.conn.ehlo()

    def teardown(self):
        self.conn.quit()

    def send(self, envelope):
        rejected = self.conn.sendmail(
            encode_address(envelope.sender),
            [encode_address(k) for k in envelope.receivers],
            envelope.string(),
        )
        return SendmailResponse(
            self.conn.noop(),
            rejected,
        )


class Postman(object): 
    """
    Encapsulates a connection to a server, created by
    some *session* class and provides middleware
    management and setup/teardown goodness.

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
            conn.setup()
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
            conn.send(envelope)
