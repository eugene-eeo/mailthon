import pytest
from mailthon.api import html
from .fixtures import postman


class Transport(object):
    def __init__(self, server, port, **kwargs):
        self.server = server
        self.port = port
        self.kwargs = kwargs

    def ehlo(self):
        pass

    def quit(self):
        pass

    def login(self, username, password):
        pass


class TestPostman:
    @pytest.fixture
    def envelope(self):
        return html(
            sender='Me <me@me.com>',
            receivers=['him@me.com', 'her@me.com'],
            subject='subject',
            content='content',
            encoding='ascii',
        )

    def test_connection(self, postman):
        with postman.connection() as conn:
            conn.ehlo()
            assert conn.noop()[0] == 250

    def test_send(self, postman, envelope):
        r = postman.send(envelope)
        assert r.ok

    def test_deliver(self, postman, envelope):
        with postman.connection() as conn:
            response = postman.deliver(conn, envelope)
            assert response.ok

    def test_use(self, postman):
        stack = []

        @postman.use
        def function(conn):
            stack.append(conn)

        with postman.connection() as conn:
            assert stack == [conn]

    def test_connect_opts(self, postman):
        postman.transport = Transport
        postman.connect_opts = {'timeout': 0}

        with postman.connection() as conn:
            assert conn.server == postman.server
            assert conn.port == postman.port
            assert conn.kwargs == postman.connect_opts
