from pytest import fixture
from mailthon.response import Response, SendmailResponse


@fixture(params=[250, 251])
def status(request):
    return request.param


@fixture
def message(status):
    return 'ok' if status == 250 else 'error'


class TestResponse:
    @fixture
    def res(self, status, message):
        return Response((status, message))

    def test_attrs(self, res, status, message):
        assert res.status_code == status
        assert res.message == message

    def test_ok(self, res, status, message):
        if status == 250:
            assert res.ok
        else:
            assert not res.ok


class TestSendmailResponse:
    @fixture(params=[1, 0])
    def failures(self, request):
        return {'addr': (251, 'error')} if request.param else {}

    def test_ok(self, failures, status, message):
        r = SendmailResponse((status, message), failures)
        if not failures and status == 250:
            assert r.ok
            assert not r.rejected
        elif failures:
            rejected = r.rejected['addr']
            assert not r.ok
            assert not rejected.ok
            assert rejected.status_code == 251
        else:
            assert not r.ok
