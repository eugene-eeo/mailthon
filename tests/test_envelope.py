import pytest
from mailthon.enclosure import PlainText
from mailthon.envelope import Envelope
from mailthon.headers import sender, to, subject
from .mimetest import mimetest


class TestEnvelope:
    @pytest.fixture
    def envelope(self):
        return Envelope(
            headers=[
                sender('Me <me@mail.com>'),
                to('him@mail.com', 'them@mail.com'),
                subject('subject'),
            ],
            enclosure=[
                PlainText('hi!'),
                PlainText('bye!'),
            ],
        )

    def test_string(self, envelope):
        mime = mimetest(envelope.string())
        assert [g.payload for g in mime.parts] == [b'hi!', b'bye!']

    def test_headers(self, envelope):
        mime = mimetest(envelope.mime())

        assert mime['Sender'] == 'Me <me@mail.com>'
        assert mime['To'] == 'him@mail.com, them@mail.com'
        assert mime['Subject'] == 'subject'

    def test_attrs(self, envelope):
        assert envelope.sender == 'Me <me@mail.com>'
        assert envelope.receivers == ['him@mail.com', 'them@mail.com']
