import pytest
from mock import Mock, call
from mailthon.api import email, postman
from mailthon.middleware import TLS, Auth
from .mimetest import mimetest
from .test_middleware import tls_started


class TestEmail:
    @pytest.fixture
    def mime(self):
        envelope = email(
            sender='Me <me@mail.com>',
            receivers=['rcv@mail.com'],
            subject='Something',
            content='<p>hi</p>',
            attachments=['tests/assets/spacer.gif'],
            cc=['cc1@mail.com', 'cc2@mail.com'],
            bcc=['bcc1@mail.com', 'bcc2@mail.com'],
            encoding='ascii',
        )
        return mimetest(envelope.mime())


    def test_bcc_not_set(self, mime):
        assert not mime['Bcc']

    def test_headers(self, mime):
        assert mime['Sender'] == 'Me <me@mail.com>'
        assert mime['To'] == 'rcv@mail.com'
        assert mime['Cc'] == 'cc1@mail.com, cc2@mail.com'
        assert mime['Date']
        assert mime['Message-ID']

    def test_payload(self, mime):
        assert [k.payload for k in mime.parts] == [
            b'<p>hi</p>',
            open('tests/assets/spacer.gif', 'rb').read(),
        ]

        assert mime.parts[0].encoding == 'us-ascii'
        assert mime.parts[1].encoding is None


class TestPostman:
    @pytest.fixture
    def postman(self):
        return postman(
            host='smtp.mail.com',
            port=100,
            auth=('username', 'password'),
            force_tls=True,
            options={'timeout': 1},
        )

    def test_attributes(self, postman):
        assert postman.host == 'smtp.mail.com'
        assert postman.port == 100
        assert postman.options == {'timeout': 1}

    def test_middleware(self, postman):
        conn = Mock()

        for item in postman.middlewares:
            item(conn)

        assert tls_started(conn)
        assert call.login('username', 'password') in conn.mock_calls
