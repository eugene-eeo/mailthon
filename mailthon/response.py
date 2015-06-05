"""
    mailthon.response
    ~~~~~~~~~~~~~~~~~

    Response objects encapsulate responses returned
    by SMTP servers.

    :copyright: (c) 2015 by Eeo Jun
    :license: MIT, see LICENSE for details.
"""

class Response(object):
    """
    Encapsulates a (status_code, message) tuple
    returned by a server when the ``NOOP``
    command is called.

    :param pair: A (status_code, message) pair.
    """

    def __init__(self, pair):
        status, message = pair
        self.status_code = status
        self.message = message

    @property
    def ok(self):
        """
        Tells whether the Response object is ok-
        that everything went well. Returns true
        if the status code is 250, false otherwise.
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

    def __init__(self, pair, rejected):
        Response.__init__(self, pair)
        self.rejected = {}
        for addr, pair in rejected.items():
            self.rejected[addr] = Response(pair)

    @property
    def ok(self):
        """
        Returns True only if no addresses were
        rejected and if the status code is 250.
        """
        return (Response.ok.fget(self) and
                not self.rejected)
