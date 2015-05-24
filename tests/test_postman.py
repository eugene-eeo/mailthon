from pytest import fixture
from mock import Mock, call
from mailthon.stamp import Stamp
from mailthon.postman import Postman
from mailthon.envelope import Envelope
from mailthon.enclosure import PlainText
from mailthon import headers


@fixture
def smtp():
    smtp = Mock()
    smtp.return_value = smtp
    smtp.noop.return_value = (250, 'ok')
    smtp.sendmail.return_value = {}
    return smtp


@fixture
def envelope():
    env = Envelope(
        stamp=Stamp([
            headers.From('Me <me@mail.com>'),
            headers.To('him@mail.com'),
            headers.Subject('Subject'),
        ]),
        enclosure=[
            PlainText('Hi!'),
        ],
    )
    info = env.info()
    mocked_info = Mock(
        sender=info.sender,
        receivers=info.receivers,
    )
    mocked_info.return_value = mocked_info
    mocked_info.string.return_value = '--email--'
    env.info = mocked_info
    return env


class TestPostman:
    host = 'smtp.mail.com'
    port = 587

    @fixture
    def postman(self, smtp):
        postman = Postman(self.host, self.port)
        postman.transport = smtp
        return postman

    def test_connection(self, postman):
        with postman.connection() as conn:
            assert conn.mock_calls == [
                call(self.host, self.port),
                call.ehlo(),
            ]

    def test_options(self, postman):
        postman.options = dict(timeout=0)

        with postman.connection() as conn:
            expected = call(self.host, self.port, timeout=0)
            assert conn.mock_calls[0] == expected

    def test_deliver(self, postman, envelope):
        with postman.connection() as conn:
            r = postman.deliver(conn, envelope)

            calls = [
                call.sendmail('Me <me@mail.com>',
                              ['him@mail.com'],
                              '--email--'),
                call.noop(),
            ]

            conn.assert_has_calls(calls, any_order=True)
            assert r.ok

    def test_send(self, postman, smtp, envelope):
        postman.deliver = Mock(return_value=1)
        assert postman.send(envelope) == 1
        assert postman.deliver.mock_calls == [
            call(smtp, envelope)
        ]

    def test_use(self, postman):
        postman.use(lambda conn: conn.login('username', 'password'))
        with postman.connection() as smtp:
            assert smtp.login.mock_calls == [call('username', 'password')]
