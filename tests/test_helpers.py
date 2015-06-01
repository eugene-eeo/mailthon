# coding=utf8
import pytest
from mailthon.helpers import guess, format_addresses, encode_address


def test_guess_recognised():
    mimetype, _ = guess('file.html', 'text/plain')
    assert mimetype == 'text/html'


def test_guess_fallback():
    mimetype, _ = guess('ha', 'text/plain')
    assert mimetype == 'text/plain'


def test_format_addresses():
    chunks = format_addresses([
        ('Sender', 'sender@mail.com'),
        'Fender <fender@mail.com>',
    ])
    assert chunks == 'Sender <sender@mail.com>, Fender <fender@mail.com>'


def test_encode_address():
    assert encode_address(u'mail@mail.com') == b'mail@mail.com'
    assert encode_address(u'mail@måil.com') == b'mail@xn--mil-ula.com'
    assert encode_address(u'måil@måil.com') == b'm\xc3\xa5il@xn--mil-ula.com'
