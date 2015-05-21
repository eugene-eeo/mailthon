import pytest
from mailthon.api import html
from mailthon.middleware import Auth
from .mocks import MyPostman, MockedSMTP


class TestPostman:
    @pytest.fixture
    def postman(self):
        return MyPostman(
            server='smtp.me.com',
            port=587,
            middlewares=[Auth('user', 'pass')],
            )

    @pytest.fixture
    def envelope(self):
        return html(
            sender='Me <me@me.com>',
            receivers=['him@me.com', 'her@me.com'],
            subject='subject',
            content='content',
            encoding='ascii',
        )

    def match_vcr(self, smtp, envelope):
        sendmail_args = (envelope.sender,
                         envelope.receivers)
        assert smtp.vcr == [
            ('ehlo', ()),
            ('login', ('user', 'pass')),
            ('sendmail', sendmail_args),
            ('noop', ()),
            ('quit', ()),
        ]
        assert smtp.closed

    def test_connection(self, postman):
        with postman.connection() as conn:
            assert conn.server == 'smtp.me.com'
            assert conn.port == 587
        assert conn.vcr == [
            ('ehlo', ()),
            ('login', ('user', 'pass')),
            ('quit', ()),
        ]

    def test_send(self, postman, envelope):
        r = postman.send(envelope)
        assert r.ok

        self.match_vcr(MockedSMTP.instance, envelope)

    def test_deliver(self, postman, envelope):
        with postman.connection() as conn:
            response = postman.deliver(conn, envelope)
            assert response.ok

        self.match_vcr(conn, envelope)

    def test_use(self, postman):
        @postman.use
        def function(conn):
            pass

        assert function in postman.middlewares
