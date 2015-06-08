import pytest
from mailthon.enclosure import PlainText
from mailthon.envelope import Envelope
from mailthon.headers import sender, to, subject
from .mimetest import mimetest


class TestEnvelope:
    @pytest.fixture
    def envelope(self):
        return Envelope(
            PlainText(
                'hi!',
                headers=[
                    sender('Me <me@mail.com>'),
                    to('him@mail.com', 'them@mail.com'),
                    subject('subject'),
                ]),
        )

    def test_mime(self, envelope):
        mime = mimetest(envelope.mime())

        assert mime['Sender'] == 'Me <me@mail.com>'
        assert mime['To'] == 'him@mail.com, them@mail.com'
        assert mime['Subject'] == 'subject'

    def test_attrs(self, envelope):
        assert envelope.sender == 'me@mail.com'
        assert envelope.receivers == ['him@mail.com', 'them@mail.com']

    def test_mail_from(self, envelope):
        envelope.mail_from = 'from@mail.com'
        assert envelope.sender == 'from@mail.com'

    def test_rcpt_to(self, envelope):
        envelope.rcpt_to = ['hi@mail.com']
        assert envelope.receivers == ['hi@mail.com']
