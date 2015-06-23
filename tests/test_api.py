import pytest
from mailthon.api import postman, email
from mailthon.middleware import Auth, TLS
from .utils import unicode as uni
from .mimetest import mimetest


class TestPostman:
    p = postman(
        host='smtp.mail.com',
        port=1000,
        auth=('username', 'password'),
        options={'key': 'value'},
    )

    def test_middlewares(self):
        tls, auth = self.p.middlewares
        assert not tls.force
        assert auth.username == 'username' and auth.password == 'password'

    def test_options(self):
        opts = dict(
            host='smtp.mail.com',
            port=1000,
            key='value',
            )
        assert self.p.options == opts


class TestEmail:
    e = email(
        subject='hi',
        sender='name <send@mail.com>',
        receivers=['rcv@mail.com'],
        cc=['rcv1@mail.com'],
        bcc=['rcv2@mail.com'],
        content='hi!',
        attachments=['tests/assets/spacer.gif'],
    )

    def test_attrs(self):
        assert self.e.sender == 'send@mail.com'
        assert set(self.e.receivers) == set([
            'rcv@mail.com',
            'rcv1@mail.com',
            'rcv2@mail.com',
            ])

    def test_headers(self):
        mime = mimetest(self.e.mime())
        assert not mime['Bcc']

    def test_content(self):
        mime = mimetest(self.e.mime())
        assert [k.payload for k in mime.parts] == [
            b'hi!',
            open('tests/assets/spacer.gif', 'rb').read()
            ]
