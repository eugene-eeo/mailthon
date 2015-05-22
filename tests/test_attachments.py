import pytest
from base64 import b64encode
from mailthon.envelope import Envelope, Stamp
from mailthon.attachments import PlainText, HTML, Image, Raw
from .fixtures import postman


class TestPlainText:
    attachment_cls = PlainText
    content_type = 'text/plain'
    headers = {'Content-ID': 'something'}
    content = 'hi'

    @pytest.fixture
    def attachment(self):
        return self.attachment_cls(
            self.content,
            encoding='ascii',
            headers=self.headers,
        )

    @pytest.fixture
    def mime(self, attachment):
        return attachment.mime()

    def test_content_type(self, mime):
        assert mime.get_content_type() == self.content_type

    def test_payload(self, mime):
        assert mime.get_payload() == self.content

    def test_headers(self, mime):
        for item in self.headers:
            assert mime[item] == self.headers[item]

    def test_sendable(self, attachment, postman):
        r = postman.send(Envelope(
            stamp=Stamp(
                sender='me <me@me.com>',
                receivers=['him@me.com'],
                subject='something',
            ),
            attachments=[attachment],
        ))
        assert r.ok


class TestHTML(TestPlainText):
    attachment_cls = HTML
    content_type = 'text/html'


class TestImage(TestPlainText):
    content_type = 'image/gif'
    content = open('tests/assets/spacer"".gif', 'rb').read()

    @pytest.fixture(scope='class')
    def attachment(self):
        return Image(self.content, headers=self.headers)

    def test_payload(self, mime):
        payload = mime.get_payload().strip()
        other = b64encode(self.content).decode()
        assert ''.join(payload.split()) == other


class TestRaw(TestImage):
    @pytest.fixture(scope='class')
    def attachment(self):
        r = Raw.from_filename('tests/assets/spacer"".gif')
        r.headers.update(self.headers)
        return r

    def test_disposition(self, mime):
        string = r'attachment; filename="spacer\"\".gif"'
        assert mime['Content-Disposition'] == string
