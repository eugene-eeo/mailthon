from sys import version_info
from pytest import fixture
from mock import Mock, call


if version_info[0] == 3:
    unicode = str
    bytes_type = bytes
else:
    unicode = lambda k: k.decode('utf8')
    bytes_type = str


def mocked_smtp(*args, **kwargs):
    smtp = Mock()
    smtp.return_value = smtp
    smtp(*args, **kwargs)
    smtp.noop.return_value = (250, 'ok')
    smtp.sendmail.return_value = {}

    def side_effect():
        smtp.closed = True

    smtp.quit.side_effect = side_effect
    return smtp


def tls_started(conn):
    calls = conn.mock_calls
    starttls = call.starttls()
    ehlo = call.ehlo()
    return (starttls in calls and
            ehlo in calls[calls.index(starttls)+1:])
