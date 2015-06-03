from pytest import fixture
from mock import Mock, call
from mailthon.postman import Postman
from mailthon.envelope import Envelope
from mailthon.enclosure import PlainText
from mailthon.headers import sender, to, subject


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
        headers=[sender('Me <me@mail.com>'),
                 to('him@mail.com'),
                 subject('subject')],
        enclosure=[PlainText('Hi!')],
    )
    env.string = Mock(return_value='--email--')
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

            sendmail = call.sendmail(
                envelope.sender.encode(),
                [k.encode() for k in envelope.receivers],
                envelope.string(),
            )
            noop = call.noop()

            conn.assert_has_calls([sendmail, noop], any_order=True)
            assert r.ok

    def test_deliver_with_failures(self, smtp, postman, envelope):
        smtp.sendmail.return_value = {
            'addr': (255, 'something-bad'),
        }

        with postman.connection() as conn:
            r = postman.deliver(conn, envelope)

            assert not r.rejected['addr'].ok
            assert not r.ok

    def test_send(self, postman, smtp, envelope):
        postman.deliver = Mock()
        postman.send(envelope)
        assert postman.deliver.mock_calls == [
            call(smtp, envelope)
        ]

    def test_use(self, postman):
        postman.use(lambda conn: conn.login('username', 'password'))
        with postman.connection() as smtp:
            assert smtp.login.mock_calls == [call('username', 'password')]
