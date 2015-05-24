import pytest
from mailthon.enclosure import PlainText
from mailthon.envelope import Envelope, Stamp, Info
from mailthon import headers
from .mimetest import mimetest, blank


@pytest.fixture
def stamp():
    return Stamp([
        headers.From('Me <me@mail.com>'),
        headers.To('him@mail.com', 'them@mail.com'),
        headers.Subject('subject'),
        headers.Header('X-This-That', 'Something'),
    ])


class TestStamp:
    def test_prepare(self, stamp):
        info = Info(blank())
        stamp.prepare(info)

        assert info.headers['To'] == 'him@mail.com, them@mail.com'
        assert info.headers['From'] == 'Me <me@mail.com>'
        assert info.headers['Subject'] == 'subject'
        assert info.headers['X-This-That'] == 'Something'


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
        mime = mimetest(envelope.info().string())
        assert [g.payload for g in mime.parts] == [b'hi!', b'bye!']

    def test_headers(self, envelope):
        mime = mimetest(envelope.info().mime)

        assert mime['From'] == 'Me <me@mail.com>'
        assert mime['To'] == 'him@mail.com, them@mail.com'
        assert mime['Subject'] == 'subject'
