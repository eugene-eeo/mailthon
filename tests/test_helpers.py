import pytest
from mailthon.helpers import inject_headers, guess, embed
from mailthon.headers import From, To, Subject, Header
from .mimetest import blank


def test_inject_headers():
    mime = blank()
    mime['X-Override'] = 'Else'
    headers = {
        'X-Something': 'Something',
        'X-Override':  'Overridden',
        }
    inject_headers(headers, mime)

    assert mime['X-Something'] == 'Something'
    assert mime['X-Override'] == 'Overridden'


def test_guess_recognised():
    mimetype, _ = guess('file.html', 'text/plain')
    assert mimetype == 'text/html'


def test_guess_fallback():
    mimetype, _ = guess('ha', 'text/plain')
    assert mimetype == 'text/plain'


@pytest.fixture
def headers():
    return (
        From('Me <me@mail.com>'),
        To('him@mail.com', 'them@mail.com'),
        Subject('subject'),
        Header('X-This-That', 'Something'),
    )


def test_embed(headers):
    mime = blank()
    info = embed(headers, mime)

    assert mime['To'] == 'him@mail.com, them@mail.com'
    assert mime['From'] == 'Me <me@mail.com>'
    assert mime['Subject'] == 'subject'
    assert mime['X-This-That'] == 'Something'
