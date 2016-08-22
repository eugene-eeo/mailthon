# -*- coding: utf-8 -*-
import pytest
from mock import Mock, call
from mailthon.api import email, postman
from mailthon.postman import Postman
from mailthon.middleware import tls, auth
from .utils import unicode as uni
from .mimetest import mimetest


class TestPostman:
    p = postman(
        host='smtp.mail.com',
        port=1000,
        auth=('username', 'password'),
        options={'key': 'value'},
    )

    def test_options(self):
        opts = dict(
            host='smtp.mail.com',
            port=1000,
            key='value',
            )
        assert self.p.options == opts


class TestRealSmtp:
    def test_send_email_example(self, smtpserver):
        host = smtpserver.addr[0]
        port = smtpserver.addr[1]
        p = Postman(host=host, port=port)

        r = p.send(email(
            content='<p>Hello 世界</p>',
            subject='Hello world',
            sender='John <john@jon.com>',
            receivers=['doe@jon.com'],
        ))

        assert r.ok
        assert len(smtpserver.outbox) == 1


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
