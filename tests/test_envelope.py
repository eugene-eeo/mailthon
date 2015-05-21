import pytest
from email import message_from_string
from mailthon.attachments import PlainText
from mailthon.envelope import Envelope, Stamp


class TestEnvelope:
    @pytest.fixture(autouse=True)
    def envelope(self):
        return Envelope(
            stamp=Stamp(sender='sender <me@mail.com>',
                        receivers=['him@mail.com'],
                        subject='hi!'),
            attachments=[
                PlainText('Hi!'),
                PlainText('Bye!'),
            ],
            headers={'This': 'him@mail.com'},
        )

    def match_headers(self, mime): 
        assert mime['Subject'] == 'hi!'
        assert mime['From'] == 'sender <me@mail.com>'
        assert mime['To'] == 'him@mail.com'
        assert mime['This'] == 'him@mail.com'

    def test_prepare(self, envelope):
        mime = envelope.prepare()
        self.match_headers(mime)

    def test_to_string(self, envelope):
        mime = message_from_string(envelope.to_string())
        self.match_headers(mime)

    def test_put_headers(self, envelope):
        headers = {}
        envelope.put_headers(headers)

        assert headers == {'This': 'him@mail.com'}
