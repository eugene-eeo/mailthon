# coding=utf8
from pytest import fixture
from mailthon.enclosure import PlainText, HTML, Binary, Attachment, Collection
from .mimetest import mimetest
from .utils import unicode


fixture = fixture(scope='class')


class TestCollection:
    @fixture
    def mime(self):
        coll = Collection(
            PlainText('1'),
            PlainText('2'),
            subtype='alternative',
            headers={
                'X-Something': 'value',
            },
        )
        return mimetest(coll.mime())

    def test_default_mimetype(self):
        mime = mimetest(Collection().mime())
        assert mime.mimetype == 'multipart/mixed'

    def test_mimetype(self, mime):
        assert mime.mimetype == 'multipart/alternative'

    def test_payload(self, mime):
        assert [p.payload for p in mime.parts] == [b'1', b'2']

    def test_headers(self, mime):
        assert mime['X-Something'] == 'value'


class TestPlainText:
    content = unicode('some-content 华语')
    headers = {
        'X-Something': 'String',
        'X-Something-Else': 'Other String',
    }
    bytes_content = content.encode('utf-8')
    expected_mimetype = 'text/plain'
    expected_encoding = 'utf-8'

    @fixture
    def enclosure(self):
        return PlainText(self.content, headers=self.headers)

    @fixture
    def mime(self, enclosure):
        return mimetest(enclosure.mime())

    def test_encoding(self, mime):
        assert mime.encoding == self.expected_encoding

    def test_mimetype(self, mime):
        assert mime.mimetype == self.expected_mimetype

    def test_content(self, mime):
        assert mime.payload == self.bytes_content

    def test_headers(self, mime):
        for header in self.headers:
            assert mime[header] == self.headers[header]


class TestHTML(TestPlainText):
    expected_mimetype = 'text/html'

    @fixture
    def enclosure(self):
        return HTML(self.content, headers=self.headers)


class TestBinary(TestPlainText):
    expected_mimetype = 'image/gif'

    with open('tests/assets/spacer.gif', 'rb') as handle:
        bytes_content = handle.read()
        content = bytes_content

    @fixture
    def enclosure(self):
        return Binary(
            content=self.content,
            mimetype=self.expected_mimetype,
            headers=self.headers,
        )

    def test_encoding(self, mime):
        assert mime.encoding is None

    def test_headers_priority(self):
        b = Binary(content=self.content,
                   mimetype=self.expected_mimetype,
                   headers={'Content-Type': 'text/plain'})
        mime = mimetest(b.mime())
        assert mime['Content-Type'] == 'text/plain'


class TestAttachment(TestBinary):
    @fixture
    def enclosure(self):
        raw = Attachment('tests/assets/spacer.gif', headers=self.headers)
        return raw

    def test_content_disposition(self, mime):
        expected = r'attachment; filename="spacer.gif"'
        assert mime['Content-Disposition'] == expected

    def test_headers_priority(self):
        a = Attachment('tests/assets/spacer.gif',
                       headers={'Content-Disposition': 'something'})
        mime = mimetest(a.mime())
        assert mime['Content-Disposition'] == 'something'


def test_binary_with_encoding():
    b = Binary(
        content=b'something',
        mimetype='image/gif',
        encoding='utf-8',
    )
    mime = mimetest(b.mime())
    assert mime.encoding == 'utf-8'
