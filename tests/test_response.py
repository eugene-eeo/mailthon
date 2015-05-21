import pytest
from mailthon.response import Response, SendmailResponse


OK_RES = (250, 'm')
NO_RES = (100, 'm')


class TestResponse:
    def test_response_ok(self):
        assert Response(OK_RES).ok
        assert not Response(NO_RES).ok

    def test_response_attrs(self):
        r = Response(OK_RES)
        assert r.status_code == 250
        assert r.message == 'm'


class TestSendmailResponse:
    def test_response_ok(self):
        assert SendmailResponse(OK_RES, {}).ok
        assert not SendmailResponse(OK_RES, {'k': NO_RES}).ok
        assert not SendmailResponse(NO_RES, {}).ok

    def test_response_rejected(self):
        res = SendmailResponse(OK_RES, {
            'fail1': NO_RES,
            'fail2': NO_RES,
        })
        for addr, r in res.rejected.items():
            assert addr in ('fail1', 'fail2')
            assert r.status_code ==  100
            assert r.message == 'm'
            assert not r.ok
