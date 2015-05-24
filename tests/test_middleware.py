from pytest import fixture
from mock import Mock, call
from mailthon.middleware import TLS, Auth


@fixture
def smtp():
    return Mock()


def tls_started(conn):
    return conn.mock_calls[-2:] == [
        call.starttls(),
        call.ehlo(),
    ]


class TestTlsSupported:
    @fixture
    def conn(self, smtp):
        smtp.has_extn.return_value = True
        return smtp

    def test_no_force(self, conn):
        tls = TLS()
        tls(conn)

        assert conn.mock_calls[0] == call.has_extn('STARTTLS')
        assert tls_started(conn)

    def test_force(self, conn):
        tls = TLS(force=True)
        tls(conn)

        assert tls_started(conn)


class TestTLSUnsupported:
    @fixture
    def conn(self, smtp):
        smtp.has_extn.return_value = False
        return smtp

    def test_no_force(self, conn):
        tls = TLS()
        tls(conn)

        assert not tls_started(conn)


class TestAuth:
    def test_auth(self, smtp):
        auth = Auth(username='user', password='pass')
        auth(smtp)

        assert smtp.mock_calls == [
            call.login('user', 'pass')
        ]
