import pytest
from mock import call, Mock
from mailthon.postman import Session
from mailthon.enclosure import PlainText
from .utils import mocked_smtp, unicode


class FakeSession(Session):
    smtp_instances = []

    def __init__(self, **kwargs):
        self.conn = mocked_smtp(**kwargs)
        self.smtp_instances.append(self.conn)


@pytest.fixture
def enclosure():
    env = PlainText(
        headers={
            'Sender': unicode('sender@mail.com'),
            'To': unicode('addr1@mail.com, addr2@mail.com'),
        },
        content='Hi!',
    )
    env.string = Mock(return_value='--string--')
    return env


class TestSession:
    host = 'host'
    port = 1000

    @pytest.fixture
    def session(self):
        return FakeSession(host=self.host,
                           port=self.port)

    def test_init(self, session):
        expected = [call(host=self.host, port=self.port)]
        assert session.conn.mock_calls == expected

    def test_setup(self, session):
        session.setup()
        assert call.ehlo() in session.conn.mock_calls

    def test_teardown(self, session):
        session.teardown()
        assert session.conn.mock_calls[-1] == call.quit()

    def test_send(self, session, enclosure):
        session.send(enclosure)
        sendmail = call.sendmail(
            b'sender@mail.com',
            [b'addr1@mail.com', b'addr2@mail.com'],
            '--string--',
        )
        assert sendmail in session.conn.mock_calls
