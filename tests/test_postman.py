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
    host = 'host'
    port = 1000

    @fixture
    def postman(self, smtp):
        p = Postman(self.host, self.port)
        p.transport = smtp
        return p

    @fixture(params=[0, 1])
    def with_failures(self, request, smtp):
        failures = request.param
        if failures:
            smtp.sendmail.return_value = {'addr': (255, 'reason')}
            smtp.noop.return_value = (250, 'ok')
        return failures

    def test_connection(self, postman, smtp):
        with postman.connection() as conn:
            assert conn is smtp
            assert conn.mock_calls == [
                call(self.host, self.port),
                call.ehlo(),
            ]

    def test_deliver_with_failures(self, postman, envelope, with_failures):
        with postman.connection() as conn:
            r = postman.deliver(conn, envelope)
            if with_failures:
                assert not r.ok
                assert r.rejected
            else:
                assert not r.rejected
                assert r.ok

    def test_deliver_mocked_calls(self, postman, envelope):
        with postman.connection() as conn:
            postman.deliver(conn, envelope)
            sendmail = call.sendmail(
                envelope.sender.encode(),
                [u.encode() for u in envelope.receivers],
                envelope.string(),
            )
            ehlo = call.ehlo()
            conn.assert_has_calls(
                [sendmail, ehlo],
                any_order=True,
            )

    def test_send(self, postman, envelope, smtp):
        postman.deliver = Mock()
        postman.send(envelope)
        assert call(smtp, envelope) in postman.deliver.mock_calls

    def test_use(self, postman):
        middleware = Mock()
        postman.use(middleware)

        with postman.connection() as conn:
            assert middleware.mock_calls == [call(conn)]
