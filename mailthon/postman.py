"""
    mailthon.postman
    ~~~~~~~~~~~~~~~~

    Implements the main Postman class.
"""


from contextlib import contextmanager
from smtplib import SMTP
from .response import SendmailResponse


class Postman(object):
    """
    Encapsulates a connection to a server and knows
    how to send MIME emails over a certain transport.
    When subclassing, change the ``transport`` and
    ``response_cls`` class variables to tweak the
    transport used and the response class, respectively.

    :param server: The address to a server.
    :param port: Port to connect to.
    :param middlewares: An iterable of middleware that
        will be used by the Postman.
    """

    transport = SMTP
    response_cls = SendmailResponse

    def __init__(self, server, port, middlewares=(), connect_opts={}):
        self.server = server
        self.port = port
        self.middlewares = list(middlewares)
        self.connect_opts = connect_opts.copy()

    def use(self, middleware):
        """
        Use a certain function/class *middleware*,
        i.e. append it to the list of middlewares,
        and return it so it can be used as a
        decorator.
        """
        self.middlewares.append(middleware)
        return middleware

    @contextmanager
    def connection(self):
        """
        A context manager that returns a connection
        to the server using some transport, defaulting
        to SMTP. The transport will be called with
        the server address and port that has been
        passed to the constructor, in that order.
        """
        conn = self.transport(self.server, self.port, **self.connect_opts)
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
            envelope.sender,
            envelope.receivers,
            envelope.to_string(),
        )
        return self.response_cls(conn.noop(), rejected)

    def send(self, envelope):
        """
        Sends an *envelope* and return a response
        object.
        """
        with self.connection() as conn:
            return self.deliver(conn, envelope)
