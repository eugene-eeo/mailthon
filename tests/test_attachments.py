from pytest import fixture
from mailthon.attachments import PlainText, HTML, Image, Raw
from .mimetest import mimetest


class TestPlainText:
    content = 'some-content 华语'
    headers = {
        'X-Something': 'String',
        'X-Something-Else': 'Other String',
    }
    bytes_content = content.encode('utf8')
    expected_mimetype = 'text/plain'

    @fixture
    def mime(self):
        attachment = PlainText(self.content, headers=self.headers)
        return mimetest(attachment.mime())

    def test_mimetype(self, mime):
        assert mime.mimetype == self.expected_mimetype

    def test_content(self, mime):
        assert mime.payload == self.bytes_content

    def test_headers(self, mime):
        for key, value in self.headers.items():
            assert mime[key] == value


class TestHTML(TestPlainText):
    expected_mimetype = 'text/html'

    @fixture
    def mime(self):
        attachment = HTML(self.content, headers=self.headers)
        return mimetest(attachment.mime())


class TestImage(TestPlainText):
    with open('tests/assets/spacer"".gif', 'rb') as handle:
        bytes_content = handle.read()
        content = bytes_content

    expected_mimetype = 'image/gif'

    @fixture
    def mime(self):
        image = Image(
            content=self.content,
            headers=self.headers,
        )
        return mimetest(image.mime())


class TestRaw(TestImage):
    @fixture
    def mime(self):
        attachment = Raw.from_filename('tests/assets/spacer"".gif')
        attachment.headers.update(self.headers)
        return mimetest(attachment.mime())

    def test_content_disposition(self, mime):
        expected = r'attachment; filename="spacer\"\".gif"'
        assert mime['Content-Disposition'] == expected
