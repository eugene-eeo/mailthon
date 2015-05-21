import pytest
from mailthon.attachments import PlainText, HTML


class TestPlainText:
    attachment_cls = PlainText
    content_type = 'text/plain'

    @pytest.fixture
    def mime(self):
        return self.attachment_cls('hi', encoding='ascii').mime()

    def test_content_type(self, mime):
        assert mime.get_content_type() == self.content_type

    def test_payload(self, mime):
        assert mime.get_payload() == 'hi'


class TestHTML:
    attachment_cls = HTML
    content_type = 'text/html'
