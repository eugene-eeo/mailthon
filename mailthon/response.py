"""
    mailthon.response
    ~~~~~~~~~~~~~~~~~

    Response objects encapsulate responses returned
    by SMTP servers.

    :copyright: (c) 2015 by Eeo Jun
    :license: MIT, see LICENSE for details.
"""

from collections import namedtuple


_ResponseBase = namedtuple('Response', ['status_code', 'reason'])


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


class SendmailResponse:
    """
    Encapsulates a (status_code, reason) tuple
    as well as a mapping of email-address to
    (status_code, reason) tuples that can be
    attained by the NOOP and the SENDMAIL
    command.

    :param pair: The response pair.
    :param rejected: Dictionary of rejected
        addresses to status-code reason pairs.
    """

    def __init__(self, status_code, reason, rejected):
        self.res = Response(status_code, reason)
        self.rejected = {}
        for addr, pair in rejected.items():
            self.rejected[addr] = Response(*pair)

    @property
    def ok(self):
        """
        Returns True only if no addresses were
        rejected and if the status code is 250.
        """
        return self.res.ok and not self.rejected
