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
from email.header import Header


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


def encode_address(addr, encoding='utf-8'):
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
    return addr


class UnicodeDict(dict):
    def __init__(self, values=(), encoding='utf-8'):
        self.encoding = encoding
        self.update(values)

    def __setitem__(self, key, value):
        if isinstance(value, bytes_type):
            value = value.decode(self.encoding)
        dict.__setitem__(self, key, value)

    update = MutableMapping.update

    def get_bytes(self, key, default=None, encoding=None):
        if key in self:
            return self[key].encode(encoding or self.encoding)
        return default
