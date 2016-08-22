from pytest import fixture
from mailthon.response import Response, SendmailResponse


@fixture(params=[250, 251])
def status(request):
    return request.param


class TestResponse:
    reason = 'error'

    @fixture
    def res(self, status):
        return Response(status, self.reason)

    def test_attrs(self, res, status):
        assert res.status_code == status
        assert res.reason == self.reason

    def test_ok(self, res, status):
        if status == 250:
            assert res.ok
        else:
            assert not res.ok


class TestSendmailResponse:
    def test_ok_with_no_failure(self):
        r = SendmailResponse(250, 'reason', {})
        assert r.ok
        assert r.rejected == {}

    def test_ok_with_failure(self):
        r = SendmailResponse(251, 'error', {})
        assert not r.ok
        assert r.rejected == {}

    def test_ok_with_rejection(self):
        for code in [250, 251]:
            r = SendmailResponse(code, 'reason', {'addr': (123, 'reason')})
            assert not r.ok
            assert r.rejected['addr'] == Response(123, 'reason')
