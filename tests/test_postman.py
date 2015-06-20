from pytest import fixture
from mock import call, Mock
from mailthon.postman import Session, Postman
from mailthon.enclosure import PlainText
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
    host = 'host'
    port = 1000

    @fixture
    def session(self):
        return FakeSession(host=self.host,
                           port=self.port)

    @fixture(params=[0, 1])
    def failures(self, request, session):
        smtp = session.conn
        failures = request.param
        if failures:
            smtp.sendmail.return_value = {'addr': (255, 'reason')}
            smtp.noop.return_value = (250, 'ok')
        return failures

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

    def test_send_with_failures(self, session, enclosure, failures):
        r = session.send(enclosure)
        if failures:
            assert not r.ok
            assert r.rejected
        else:
            assert r.ok
            assert not r.rejected


class TestPostman:
    @fixture
    def postman(self):
        def config(**kwargs):
            session.opts = kwargs
            return session

        session = Mock(spec=Session)
        session.side_effect = config

        return Postman(
            session=session,
            host='host',
            port=1000,
            )

    def test_connection(self, postman):
        with postman.connection() as session:
            assert session.opts == {'host': 'host', 'port': 1000}
            assert session.mock_calls == [call(**postman.options),
                                          call.setup()]
        assert session.mock_calls[-1] == call.teardown()

    def test_use(self, postman):
        func = Mock()
        assert postman.use(func) is func

        with postman.connection() as session:
            assert func.mock_calls == [call(session)]

    def test_send(self, postman, enclosure):
        postman.send(enclosure)
        assert call.send(enclosure) in postman.session.mock_calls
