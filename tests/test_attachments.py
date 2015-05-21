import pytest
from base64 import b64encode
from mailthon.attachments import PlainText, HTML, Image


class TestPlainText:
    attachment_cls = PlainText
    content_type = 'text/plain'
    content = 'hi'

    @pytest.fixture
    def mime(self):
        return self.attachment_cls(self.content, encoding='ascii').mime()

    def test_content_type(self, mime):
        assert mime.get_content_type() == self.content_type

    def test_payload(self, mime):
        assert mime.get_payload() == self.content


class TestHTML(TestPlainText):
    attachment_cls = HTML
    content_type = 'text/html'


class TestImage(TestPlainText):
    content_type = 'image/gif'
    content = open('tests/assets/spacer.gif', 'rb').read()

    @pytest.fixture
    def mime(self):
        return Image(self.content).mime()

    def test_payload(self, mime):
        pass
