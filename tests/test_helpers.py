from mailthon.helpers import inject_headers
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
