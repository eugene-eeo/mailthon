"""
    mailthon.helpers
    ~~~~~~~~~~~~~~~~

    Implements various helper functions/utilities.

    :copyright: (c) 2015 by Eeo Jun
    :license: MIT, see LICENSE for details.
"""

import mimetypes


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
