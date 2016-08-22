from pytest import fixture, mark
from mock import Mock, call
from mailthon.middleware import tls, auth
from .utils import tls_started


@fixture
def smtp():
    return Mock()


class TestTlsSupported:
    @fixture
    def conn(self, smtp):
        smtp.has_extn.return_value = True
        return smtp

    @mark.parametrize('force', [True, False])
    def test_force(self, conn, force):
        wrap = tls(force=force)
        wrap(conn)

        if not force:
            assert conn.mock_calls[0] == call.has_extn('STARTTLS')
        assert tls_started(conn)


class TestTLSUnsupported:
    @fixture
    def conn(self, smtp):
        smtp.has_extn.return_value = False
        return smtp

    def test_no_force(self, conn):
        wrap = tls()
        wrap(conn)

        assert not tls_started(conn)


class TestAuth:
    def test_logs_in_user(self, smtp):
        wrap = auth('user', 'pass')
        wrap(smtp)

        assert call.login('user', 'pass') in smtp.mock_calls
