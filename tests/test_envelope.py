import pytest
from mock import Mock
from email.mime.base import MIMEBase
from mailthon.enclosure import PlainText
from mailthon.envelope import Envelope
from .mimetest import mimetest


class TestEnvelope:
    @pytest.fixture
    def embedded(self):
        pt = PlainText(
            content='hi',
            headers={
                'Sender': 'me@mail.com',
                'To': 'him@mail.com, them@mail.com',
                }
            )
        mime = Mock()
        mime.as_string = Mock(return_value='--email--')
        pt.mime = Mock(return_value=mime)
        return pt

    @pytest.fixture
    def envelope(self, embedded):
        return Envelope(embedded)

    def test_mime(self, envelope, embedded):
        assert envelope.mime() == embedded.mime()
        assert envelope.string() == embedded.string()

    def test_attrs(self, envelope, embedded):
        assert envelope.sender == embedded.sender
        assert envelope.receivers == embedded.receivers

    def test_mail_from(self, envelope):
        envelope.mail_from = 'from@mail.com'
        assert envelope.sender == 'from@mail.com'

    def test_rcpt_to(self, envelope):
        envelope.rcpt_to = ['hi@mail.com']
        assert envelope.receivers == ['hi@mail.com']
