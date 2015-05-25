"""
    mailthon.middleware
    ~~~~~~~~~~~~~~~~~~~

    Implements Middleware classes. Middleware are small and
    configurable pieces of code that implement and allow for
    certain functionality.

    :copyright: (c) 2015 by Eeo Jun
    :license: MIT, see LICENSE for details.
"""

class Middleware(object):
    """
    Base class for middlewares. Middlewares are encouraged
    to subclass from this class and override the ``__call__``
    method to implement the correct functionality. By
    default, the ``__call__`` method raises
    NotImplementedError.
    """

    def __call__(self, conn):
        """
        To be overriden. The Postman class will call this
        method with a connection object.
        """
        raise NotImplementedError


class TLS(Middleware):
    """
    Middleware implementing TLS for SMTP connections. By
    default this is not forced- TLS is only used if
    STARTTLS is available. If the *force* parameter is set
    to True, it will not query the server for TLS features
    before upgrading to TLS.
    """

    def __init__(self, force=False):
        self.force = force

    def __call__(self, conn):
        if self.force or conn.has_extn('STARTTLS'):
            conn.starttls()
            conn.ehlo()


class Auth(Middleware):
    """
    Middleware implementing authentication via LOGIN.
    Most of the time this middleware needs to be placed
    *after* TLS.

    :param username: Username to login with.
    :param password: Password of the user.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __call__(self, conn):
        conn.login(self.username,
                   self.password)
