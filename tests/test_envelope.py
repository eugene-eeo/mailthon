from pytest import fixture
from base64 import b64decode
from email import message_from_string
from mailthon.attachments import PlainText
from mailthon.envelope import Envelope, Stamp


@fixture
def stamp():
    return Stamp(sender='sender <me@mail.com>',
                 receivers=['him@mail.com', 'them@mail.com'],
                 headers={'This': 'him@mail.com'},
                 subject='hi!')


@fixture
def envelope(stamp):
    return Envelope(
        stamp=stamp,
        attachments=[
            PlainText('Hi!', encoding='utf8'),
            PlainText('Bye!', encoding='utf8'),
        ],
    )


def match_headers(mime):
    assert mime['Subject'] == 'hi!'
    assert mime['From'] == 'sender <me@mail.com>'
    assert mime['To'] == 'him@mail.com, them@mail.com'
    assert mime['This'] == 'him@mail.com'


def match_content(mime):
    text = [b64decode(m.get_payload()) for m in mime.get_payload()]
    assert text == [b'Hi!', b'Bye!']


class TestStamp:
    def test_prepare(self, stamp):
        headers = {}
        stamp.prepare(headers)
        match_headers(headers)

    def test_receiver_string(self, stamp):
        assert stamp.receiver_string == 'him@mail.com, them@mail.com'

    def test_headers_overrides_everything(self, stamp):
        stamp.headers['From'] = 'me'
        headers = {}
        stamp.prepare(headers)
        assert headers['From'] == 'me'


class TestEnvelope:
    def test_prepare(self, envelope):
        mime = envelope.prepare()
        match_headers(mime)
        match_content(mime)

    def test_to_string(self, envelope):
        mime = message_from_string(envelope.to_string())
        match_headers(mime)
        match_content(mime)
