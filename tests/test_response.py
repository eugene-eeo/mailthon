import pytest
from mailthon.response import Response, SendmailResponse


@pytest.fixture(params=(250, 255))
def reply(request):
    return (request.param, 'message')


@pytest.fixture(params=[(), {'addr': (255, 'reason')}])
def rejected(request):
    return dict(request.param)


class TestResponse:
    def test_ok(self, reply):
        r = Response(reply)
        if reply[0] == 250:
            assert r.ok
        else:
            assert not r.ok

    def test_attributes(self, reply):
        r = Response(reply)
        assert reply == (r.status_code, r.message)


class TestSendmailResponse:
    def test_ok(self, reply, rejected):
        r = SendmailResponse(reply, rejected)
        if reply[0] == 250 and not rejected:
            assert r.ok
        else:
            assert not r.ok

    def test_rejected(self, reply, rejected):
        r = SendmailResponse(reply, rejected)
        if rejected:
            r2 = r.rejected['addr']

            assert (r2.status_code, r2.message) == rejected['addr']
            assert not r2.ok
