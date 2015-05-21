import pytest
from base64 import b64encode
from textwrap import wrap
from mailthon.attachments import PlainText, HTML, Image, Raw


class TestPlainText:
    attachment_cls = PlainText
    content_type = 'text/plain'
    headers = {'Content-ID': 'something'}
    content = 'hi'

    @pytest.fixture
    def mime(self):
        attachment = self.attachment_cls(
            self.content,
            encoding='ascii',
            headers=self.headers,
        )
        return attachment.mime()

    def test_content_type(self, mime):
        assert mime.get_content_type() == self.content_type

    def test_payload(self, mime):
        assert mime.get_payload() == self.content

    def test_headers(self, mime):
        for item in self.headers:
            assert mime[item] == self.headers[item]


class TestHTML(TestPlainText):
    attachment_cls = HTML
    content_type = 'text/html'


class TestImage(TestPlainText):
    content_type = 'image/gif'
    content = open('tests/assets/spacer"".gif', 'rb').read()

    @pytest.fixture(scope='class')
    def mime(self):
        attachment = Image(self.content, headers=self.headers)
        return attachment.mime()

    def test_payload(self, mime):
        payload = mime.get_payload().strip()
        other = b64encode(self.content).decode()
        assert payload == '\n'.join(wrap(other, 76))


class TestRaw(TestImage):
    @pytest.fixture(scope='class')
    def mime(self):
        r = Raw.from_filename('tests/assets/spacer"".gif')
        r.headers.update(self.headers)
        return r.mime()

    def test_disposition(self, mime):
        string = r'attachment; filename="spacer\"\".gif"'
        assert mime['Content-Disposition'] == string

    def test_payload(self, mime):
        assert mime.get_payload() == b64encode(self.content).decode()
