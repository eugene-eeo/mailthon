"""
    mailthon.helpers
    ~~~~~~~~~~~~~~~~

    Implements various helper functions/utilities.

    :copyright: (c) 2015 by Eeo Jun
    :license: MIT, see LICENSE for details.
"""

import sys
import mimetypes
from collections import MutableMapping
from email.utils import formataddr


if sys.version_info[0] == 3:
    bytes_type = bytes
else:
    bytes_type = str


def guess(filename, fallback='application/octet-stream'):
    """
    Using the mimetypes library, guess the mimetype and
    encoding for a given *filename*. If the mimetype
    cannot be guessed, *fallback* is assumed instead.

    :param filename: Filename- can be absolute path.
    :param fallback: A fallback mimetype.
    """
    guessed, encoding = mimetypes.guess_type(filename, strict=False)
    if guessed is None:
        return fallback, encoding
    return guessed, encoding


def format_addresses(addrs):
    """
    Given an iterable of addresses or name-address
    tuples *addrs*, return a header value that joins
    all of them together with a space and a comma.
    """
    return ', '.join(
        formataddr(item) if isinstance(item, tuple) else item
        for item in addrs
    )


def stringify_address(addr, encoding='utf-8'):
    """
    Given an email address *addr*, try to encode
    it with ASCII. If it's not possible, encode
    the *local-part* with the *encoding* and the
    *domain* with IDNA.

    The result is a unicode string with the domain
    encoded as idna.
    """
    if isinstance(addr, bytes_type):
        return addr
    try:
        addr = addr.encode('ascii')
    except UnicodeEncodeError:
        if '@' in addr:
            localpart, domain = addr.split('@', 1)
            addr = b'@'.join([
                localpart.encode(encoding),
                domain.encode('idna'),
            ])
        else:
            addr = addr.encode(encoding)
    return addr.decode('utf-8')


class UnicodeDict(dict):
    """
    A dictionary that handles unicode values
    magically - that is, byte-values are
    automatically decoded. Accepts a dict
    or iterable *values*.
    """

    def __init__(self, values=(), encoding='utf-8'):
        dict.__init__(self)
        self.encoding = encoding
        self.update(values)

    def __setitem__(self, key, value):
        if isinstance(value, bytes_type):
            value = value.decode(self.encoding)
        dict.__setitem__(self, key, value)

    update = MutableMapping.update
