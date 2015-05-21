import pytest
from mailthon.middleware import TLS, Auth
from .mocks import MockedSMTP


@pytest.fixture
def smtp():
    return MockedSMTP('server', 10)


class TestTLS:
    def test_tls_force(self, smtp):
        tls = TLS(force=True)
        tls(smtp)
        assert smtp.vcr == [
            ('starttls', ()),
            ('ehlo', ()),
        ]

    def test_tls(self, smtp):
        tls = TLS()
        tls(smtp)
        assert smtp.vcr[0] == ('has_extn', ('STARTTLS',))


class TestAuth:
    def test_auth(self, smtp):
        auth = Auth(username='user', password='pass')
        auth(smtp)
        assert smtp.vcr == [
            ('login', ('user', 'pass')),
        ]
