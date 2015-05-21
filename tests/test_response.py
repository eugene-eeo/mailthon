import pytest
from mailthon.response import Response, SendmailResponse


class TestResponse:
    def test_response_ok(self):
        assert Response((250, 'm')).ok
        assert not Response((100, 'm')).ok

    def test_response_attrs(self):
        r = Response((250, 'm'))
        assert r.status_code == 250
        assert r.message == 'm'


class TestSendmailResponse:
    def test_response_ok(self):
        assert SendmailResponse((250, 'm'), {}).ok
        assert not SendmailResponse((250, 'm'), {'k': (255, 'm')}).ok
        assert not SendmailResponse((255, 'm'), {}).ok

    def test_response_rejected(self):
        res = SendmailResponse((250, 'm'), {
            'fail1': (255, 'reason'),
            'fail2': (255, 'reason'),
        })
        for addr, r in res.rejected.items():
            assert addr in ('fail1', 'fail2')
            assert r.status_code == 255
            assert r.message == 'reason'
            assert not r.ok
