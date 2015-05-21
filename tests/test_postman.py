import pytest
from mailthon.api import html
from .mocks import MyPostman, MockedSMTP


class TestPostman:
    @pytest.fixture
    def postman(self):
        return MyPostman('smtp.me.com', 587)

    @pytest.fixture
    def envelope(self):
        return html(
            sender='Me <me@me.com>',
            receivers=['him@me.com', 'her@me.com'],
            subject='subject',
            content='content',
            encoding='ascii',
        )

    def test_connection(self, postman):
        with postman.connection() as conn:
            assert conn.server == 'smtp.me.com'
            assert conn.port == 587
        assert conn.vcr == [
            ('ehlo', ()),
            ('quit', ()),
        ]

    def test_send(self, postman, envelope):
        r = postman.send(envelope)
        assert r.ok

        sendmail_args = (envelope.sender,
                         envelope.receivers)

        smtp = MockedSMTP.instance
        actions = smtp.vcr
        assert actions == [
            ('ehlo', ()),
            ('sendmail', sendmail_args),
            ('noop', ()),
            ('quit', ()),
        ]
        assert smtp.closed
