import pytest
from mock import Mock, call
import mailthon.headers as headers
from mailthon.headers import cc, bcc, content_id, content_disposition, date


def test_cc():
    assert list(cc('a')) == ['Cc', 'a']
    assert list(cc('a', 'b')) == ['Cc', 'a, b']


def test_bcc():
    assert list(bcc('a')) == ['Bcc', 'a']
    assert list(bcc('a', 'b')) == ['Bcc', 'a, b']


def test_content_id():
    assert list(content_id('spacer')) == ['Content-ID', '<spacer>']


def test_content_disposition():
    header = content_disposition('attachment', 'filename""')
    expect = ['Content-Disposition', r'attachment; filename="filename\"\""']
    assert list(header) == expect


def test_date():
    headers.formatdate = Mock(return_value=1)

    assert list(date('Today')) == ['Date', 'Today']
    assert list(date()) == ['Date', 1]

    assert headers.formatdate.mock_calls == [
        call(localtime=True),
    ]
