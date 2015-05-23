# coding=utf8
from pytest import fixture
from mailthon.enclosure import PlainText, HTML, Binary, Attachment
from .mimetest import mimetest


fixture = fixture(scope='class')


class TestPlainText:
    content = u'some-content 华语'
    headers = {
        'X-Something': 'String',
        'X-Something-Else': 'Other String',
    }
    bytes_content = content.encode('utf-8')
    expected_mimetype = 'text/plain'

    @fixture
    def enclosure(self):
        return PlainText(self.content, headers=self.headers)

    @fixture
    def mime(self, enclosure):
        return mimetest(enclosure.mime())

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
    def enclosure(self):
        return HTML(self.content, headers=self.headers)


class TestBinary(TestPlainText):
    expected_mimetype = 'image/gif'

    with open('tests/assets/spacer"".gif', 'rb') as handle:
        bytes_content = handle.read()
        content = bytes_content

    @fixture
    def enclosure(self):
        return Binary(
            content=self.content,
            mimetype=self.expected_mimetype,
            headers=self.headers,
        )


class TestAttachment(TestBinary):
    @fixture
    def enclosure(self):
        raw = Attachment('tests/assets/spacer"".gif')
        raw.headers.update(self.headers)
        return raw

    def test_content_disposition(self, mime):
        expected = r'attachment; filename="spacer\"\".gif"'
        assert mime['Content-Disposition'] == expected
