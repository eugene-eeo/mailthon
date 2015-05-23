import pytest
from mailthon.enclosure import PlainText
from mailthon.envelope import Envelope, Stamp
from mailthon import headers
from .mimetest import mimetest, blank


@pytest.fixture
def stamp():
    return Stamp(
        subject='subject',
        sender='Me <me@mail.com>',
        receivers=['him@mail.com', 'them@mail.com'],
        headers={
            'X-This-That': 'Something',
        }
    )


class TestStamp:
    def test_receiver_string(self, stamp):
        assert stamp.receiver_string == 'him@mail.com, them@mail.com'

    def test_prepare(self, stamp):
        mime = blank()
        stamp.prepare(mime)

        assert mime['To'] == 'him@mail.com, them@mail.com'
        assert mime['From'] == 'Me <me@mail.com>'
        assert mime['Subject'] == 'subject'
        assert mime['X-This-That'] == 'Something'

    def test_headers_priority(self, stamp):
        stamp.headers = {
            'To': 'her@mail.com',
            'From': 'Her <her@mail.com>'
        }

        mime = blank()
        stamp.prepare(mime)
        assert mime['To'] == 'her@mail.com'
        assert mime['From'] == 'Her <her@mail.com>'

    def test_init_with_list(self):
        stamp = Stamp(
            subject='Subject',
            sender='Me <me@mail.com>',
            receivers=['someone'],
            headers=[
                headers.date('this'),
                headers.content_id('filename'),
            ]
        )
        mime = blank()
        stamp.prepare(mime)
        assert mime['Date'] == 'this'
        assert mime['Content-ID'] == '<filename>'


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
        mime = mimetest(envelope.to_string())
        assert [g.payload for g in mime.parts] == [b'hi!', b'bye!']

    def test_headers(self, envelope):
        mime = mimetest(envelope.mime())

        assert mime['From'] == envelope.sender
        assert mime['To'] == envelope.stamp.receiver_string
        assert mime['Subject'] == envelope.stamp.subject
