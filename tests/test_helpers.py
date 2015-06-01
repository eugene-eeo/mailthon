# coding=utf8
import pytest
from mailthon.helpers import guess, format_addresses, encode_address, UnicodeDict
from .utils import unicode as uni


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
    assert encode_address(uni('mail@mail.com')) == b'mail@mail.com'
    assert encode_address(uni('mail@måil.com')) == b'mail@xn--mil-ula.com'
    assert encode_address(uni('måil@måil.com')) == b'm\xc3\xa5il@xn--mil-ula.com'


class TestUnicodeDict:
    @pytest.fixture
    def mapping(self):
        return UnicodeDict({'Item': uni('måil')})

    def test_setitem(self):
        u = UnicodeDict()
        u['Item'] = b'm\xc3\xa5il'
        assert u['Item'] == uni('måil')

    def test_getitem(self, mapping):
        assert mapping['Item'] == uni('måil')

    def test_update(self, mapping):
        mapping.update({
            'Item-1': uni('unicode-itém'),
            'Item-2': b'bytes-item',
        })
        assert mapping['Item-1'] == uni('unicode-itém')
        assert mapping['Item-2'] == uni('bytes-item')

    def test_get(self, mapping):
        assert mapping.get('Something', default=None) is None
        assert mapping.get('Item') == uni('måil')

    def test_get_bytes_encoding(self, mapping):
        with pytest.raises(UnicodeEncodeError):
            mapping.get_bytes('Item', encoding='ascii')

    def test_get_bytes(self, mapping):
        assert mapping.get_bytes('Item') == b'm\xc3\xa5il'
