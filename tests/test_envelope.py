from pytest import fixture
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
            PlainText('Hi!'),
            PlainText('Bye!'),
        ],
    )


def match_headers(mime):
    assert mime['Subject'] == 'hi!'
    assert mime['From'] == 'sender <me@mail.com>'
    assert mime['To'] == 'him@mail.com, them@mail.com'
    assert mime['This'] == 'him@mail.com'


class TestStamp:
    def test_prepare(self, stamp):
        headers = {}
        stamp.prepare(headers)
        match_headers(headers)

    def test_receiver_string(self, stamp):
        assert stamp.receiver_string == 'him@mail.com, them@mail.com'


class TestEnvelope:
    def test_prepare(self, envelope):
        mime = envelope.prepare()
        match_headers(mime)

    def test_to_string(self, envelope):
        mime = message_from_string(envelope.to_string())
        match_headers(mime)
