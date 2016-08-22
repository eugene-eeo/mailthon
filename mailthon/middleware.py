"""
    mailthon.middleware
    ~~~~~~~~~~~~~~~~~~~

    Implements Middleware classes. Middleware are small and
    configurable pieces of code that implement and allow for
    certain functionality.

    :copyright: (c) 2015 by Eeo Jun
    :license: MIT, see LICENSE for details.
"""


def tls(force=False):
    """
    Middleware implementing TLS for SMTP connections. By
    default this is not forced- TLS is only used if
    STARTTLS is available. If the *force* parameter is set
    to True, it will not query the server for TLS features
    before upgrading to TLS.
    """
    def middleware(conn):
        if force or conn.has_extn('STARTTLS'):
            conn.starttls()
            conn.ehlo()
    return middleware


def auth(username, password):
    """
    Middleware implementing authentication via LOGIN.
    Most of the time this middleware needs to be placed
    *after* TLS.

    :param username: Username to login with.
    :param password: Password of the user.
    """
    def middleware(conn):
        conn.login(username, password)
    return middleware
