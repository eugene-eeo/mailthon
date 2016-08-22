# -*- encoding: utf-8 -*-

import pytest
from mock import Mock, call
import mailthon.headers
from mailthon.headers import (Headers, cc, to, bcc, sender,
                              message_id, date, content_id,
                              content_disposition)
from .mimetest import blank


class TestNotResentHeaders:
    @pytest.fixture
    def headers(self):
        return Headers([
            ('From', 'from@mail.com'),
            sender('sender@mail.com'),
            to('to@mail.com'),
            cc('cc1@mail.com', 'cc2@mail.com'),
            bcc('bcc1@mail.com', 'bcc2@mail.com'),
        ])

    @pytest.fixture
    def content_disposition_headers(self):
        return (Headers([content_disposition("attachment", "ascii.filename")]),
                Headers([content_disposition("attachment", "файл.filename")]))

    def test_getitem(self, headers):
        assert headers['From'] == 'from@mail.com'
        assert headers['Sender'] == 'sender@mail.com'
        assert headers['To'] == 'to@mail.com'

    def test_sender(self, headers):
        assert headers.sender == 'sender@mail.com'

    def test_receivers(self, headers):
        assert set(headers.receivers) == set([
            'to@mail.com',
            'cc1@mail.com',
            'cc2@mail.com',
            'bcc1@mail.com',
            'bcc2@mail.com',
            ])

    def test_resent(self, headers):
        assert not headers.resent

    def test_prepare(self, headers):
        mime = blank()
        headers.prepare(mime)

        assert not mime['Bcc']
        assert mime['Cc'] == 'cc1@mail.com, cc2@mail.com'
        assert mime['To'] == 'to@mail.com'
        assert mime['Sender'] == 'sender@mail.com'

    def test_content_disposition_headers(self, content_disposition_headers):
        """
        Do the same as test above but for `complex` headers which can contain additional fields
        """
        for header in content_disposition_headers:
            mime = blank()
            header.prepare(mime)
            assert "filename" in mime["Content-Disposition"]


class TestResentHeaders(TestNotResentHeaders):
    @pytest.fixture
    def headers(self):
        head = TestNotResentHeaders.headers(self)
        head.update({
            'Resent-Date': 'Today',
            'Resent-From': 'rfrom@mail.com',
            'Resent-To': 'rto@mail.com',
            'Resent-Cc': 'rcc@mail.com',
            'Resent-Bcc': 'rbcc1@mail.com, rbcc2@mail.com'
        })
        return head

    def test_sender(self, headers):
        assert headers.sender == 'rfrom@mail.com'

    def test_prefers_resent_sender(self, headers):
        headers['Resent-Sender'] = 'rsender@mail.com'
        assert headers.sender == 'rsender@mail.com'

    def test_resent_sender_without_senders(self, headers):
        del headers['Resent-From']
        assert headers.sender is None

    def test_receivers(self, headers):
        assert set(headers.receivers) == set([
            'rto@mail.com',
            'rcc@mail.com',
            'rbcc1@mail.com',
            'rbcc2@mail.com',
        ])

    def test_resent(self, headers):
        assert headers.resent

    def test_resent_date_removed(self, headers):
        headers.pop('Resent-Date')
        assert not headers.resent

    def test_prepare(self, headers):
        mime = blank()
        headers.prepare(mime)

        assert not mime['Resent-Bcc']
        assert not mime['Bcc']


@pytest.mark.parametrize('function', [to, cc, bcc])
def test_tuple_headers(function):
    _, value = function(
        ('Sender', 'sender@mail.com'),
        'Me <me@mail.com>',
    )
    expected = 'Sender <sender@mail.com>, Me <me@mail.com>'
    assert value == expected


@pytest.mark.parametrize('argtype', [str, tuple])
def test_sender_tuple(argtype):
    param = (
        'name <mail@mail.com>' if argtype is str else
        ('name', 'mail@mail.com')
    )
    _, value = sender(param)
    assert value == 'name <mail@mail.com>'


def test_message_id():
    def msgid(thing=None):
        return thing

    mailthon.headers.make_msgid = Mock(side_effect=msgid)
    assert tuple(message_id()) == ('Message-ID', None)
    assert tuple(message_id('string')) == ('Message-ID', 'string')
    assert tuple(message_id(idstring=1)) == ('Message-ID', 1)


def test_date():
    formatdate = mailthon.headers.formatdate = Mock(return_value=1)
    assert tuple(date()) == ('Date', 1)
    assert formatdate.mock_calls == [call(localtime=True)]

    assert tuple(date('time')) == ('Date', 'time')


def test_content_id():
    assert dict([content_id('l')]) == {'Content-ID': '<l>'}
