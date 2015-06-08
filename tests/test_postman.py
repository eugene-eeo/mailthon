from pytest import fixture
from mock import Mock, call
from mailthon.postman import Postman
from mailthon.enclosure import Collection
from mailthon.headers import sender, to, subject
from .utils import smtp


@fixture
def enclosure():
    env = Collection(
        headers=[sender('Me <me@mail.com>'),
                 to('him@mail.com'),
                 subject('subject')]
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
    def failures(self, request, smtp):
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
        assert conn.closed

    def test_deliver_with_failures(self, postman, enclosure, failures):
        with postman.connection() as conn:
            r = postman.deliver(conn, enclosure)
            if failures:
                assert not r.ok
                assert r.rejected
            else:
                assert not r.rejected
                assert r.ok

    def test_deliver_mocked_calls(self, postman, enclosure):
        with postman.connection() as conn:
            postman.deliver(conn, enclosure)
            sendmail = call.sendmail(
                enclosure.sender.encode(),
                [u.encode() for u in enclosure.receivers],
                enclosure.string(),
            )
            ehlo = call.ehlo()
            conn.assert_has_calls(
                [sendmail, ehlo],
                any_order=True,
            )

    def test_send(self, postman, enclosure, smtp):
        deliver = postman.deliver = Mock()
        postman.send(enclosure)
        assert deliver.mock_calls == [call(smtp, enclosure)]

    def test_use(self, postman):
        middleware = Mock()
        postman.use(middleware)

        with postman.connection() as conn:
            assert middleware.mock_calls == [call(conn)]
