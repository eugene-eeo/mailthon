"""
    mailthon.response
    ~~~~~~~~~~~~~~~~~

    Response objects encapsulate responses returned
    by SMTP servers.

    :copyright: (c) 2015 by Eeo Jun
    :license: MIT, see LICENSE for details.
"""

from collections import namedtuple


_ResponseBase = namedtuple('Response', ['status_code', 'message'])


class Response(_ResponseBase):
    """
    Encapsulates a (status_code, message) tuple
    returned by a server when the ``NOOP``
    command is called.

    :param status_code: status code returned by server.
    :param message: error/success message.
    """

    @property
    def ok(self):
        """
        Returns true if the status code is 250, false
        otherwise.
        """
        return self.status_code == 250


class SendmailResponse(Response):
    """
    Encapsulates a (status_code, message) tuple
    as well as a mapping of email-address to
    (status_code, message) tuples that can be
    attained by the NOOP and the SENDMAIL
    command.

    :param pair: The response pair.
    :param rejected: Dictionary of rejected
        addresses to status-code message pairs.
    """

    def __new__(cls, status_code, message, rejected):
        self = Response.__new__(cls, status_code, message)
        self.rejected = {}
        for addr, pair in rejected.items():
            self.rejected[addr] = Response(*pair)
        return self

    @property
    def ok(self):
        """
        Returns True only if no addresses were
        rejected and if the status code is 250.
        """
        return (Response.ok.fget(self) and
                not self.rejected)
