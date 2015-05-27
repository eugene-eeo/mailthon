import pytest
from mailthon.helpers import guess, format_addresses


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
