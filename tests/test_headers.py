import pytest
from mailthon.headers import Headers
from .mimetest import blank


class TestNotResentHeaders:
    @pytest.fixture
    def headers(self):
        return Headers({
            'Sender': 'sender@mail.com',
            'From': 'from@mail.com',
            'To': 'to@mail.com',
            'Cc': 'cc1@mail.com, cc2@mail.com',
            'Bcc': 'bcc1@mail.com, bcc2@mail.com',
        })

    def test_getitem(self, headers):
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
        assert mime['From'] == 'from@mail.com'


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
