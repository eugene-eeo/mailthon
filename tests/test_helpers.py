from mailthon.helpers import inject_headers, guess
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
