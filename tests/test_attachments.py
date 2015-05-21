import pytest
from base64 import b64encode
from mailthon.attachments import PlainText, HTML, Image


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
    content = open('tests/assets/spacer.gif', 'rb').read()

    @pytest.fixture
    def mime(self):
        attachment = Image(self.content, headers=self.headers)
        return attachment.mime()

    def test_payload(self, mime):
        pass
