from mock import call, Mock
from pytest import fixture
from mailthon.enclosure import PlainText
from mailthon.postman import Session, Postman
from mailthon.response import SendmailResponse
from .utils import mocked_smtp, unicode


class FakeSession(Session):
    def __init__(self, **kwargs):
        self.opts = kwargs
        self.conn = mocked_smtp(**kwargs)


@fixture
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
    @fixture
    def session(self):
        return FakeSession(host='host',
                           port=1000)

    def test_teardown(self, session):
        session.teardown()
        assert session.conn.mock_calls[-1] == call.quit()

    def test_send(self, session, enclosure):
        smtp = session.conn
        smtp.sendmail.return_value = {}
        smtp.noop.return_value = (250, 'ok')

        response = session.send(enclosure)
        sendmail = call.sendmail(
            'sender@mail.com',
            ['addr1@mail.com', 'addr2@mail.com'],
            '--string--',
        )
        assert sendmail in session.conn.mock_calls
        assert response.ok

    def test_send_with_failures(self, session, enclosure):
        rejected = {'addr': (255, 'reason')}
        smtp = session.conn
        smtp.sendmail.return_value = rejected
        smtp.noop.return_value = (250, 'ok')

        response = session.send(enclosure)
        assert not response.ok


class TestPostman:
    @fixture
    def postman(self):
        def config(**kwargs):
            session.opts = kwargs
            return session

        session = Mock(spec=Session)
        session.side_effect = config
        session.send.return_value = SendmailResponse(250, 'ok', {})

        return Postman(
            session=session,
            host='host',
            port=1000,
            )

    def test_connection(self, postman):
        with postman.connection() as session:
            mc = session.mock_calls
            assert session.opts == {'host': 'host', 'port': 1000}
            assert mc == [call(**postman.options)]
        assert mc[-1] == call.teardown()

    def test_use(self, postman):
        func = Mock()
        assert postman.use(func) is func

        with postman.connection() as session:
            assert func.mock_calls == [call(session)]

    def test_send(self, postman, enclosure):
        r = postman.send(enclosure)
        assert call.send(enclosure) in postman.session.mock_calls
        assert r.ok
        assert not r.rejected
