import pytest
from mailthon.enclosure import PlainText
from mailthon.envelope import Envelope
from .mimetest import mimetest
from .test_stamp import stamp


class TestEnvelope:
    @pytest.fixture
    def envelope(self, stamp):
        return Envelope(
            stamp=stamp,
            enclosure=[
                PlainText('hi!'),
                PlainText('bye!'),
            ],
        )

    def test_as_string(self, envelope):
        print(envelope.info())
        mime = mimetest(envelope.info().string())
        assert [g.payload for g in mime.parts] == [b'hi!', b'bye!']

    def test_headers(self, envelope):
        mime = mimetest(envelope.info().mime)

        assert mime['From'] == 'Me <me@mail.com>'
        assert mime['To'] == 'him@mail.com, them@mail.com'
        assert mime['Subject'] == 'subject'
