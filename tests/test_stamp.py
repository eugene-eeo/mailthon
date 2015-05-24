import pytest
import mailthon.headers as headers
from mailthon.stamp import Stamp
from .mimetest import blank


@pytest.fixture
def stamp():
    return Stamp([
        headers.From('Me <me@mail.com>'),
        headers.To('him@mail.com', 'them@mail.com'),
        headers.Subject('subject'),
        headers.Header('X-This-That', 'Something'),
    ])


class TestStamp:
    def test_prepare(self, stamp):
        mime = blank()
        stamp.prepare(mime)

        assert mime['To'] == 'him@mail.com, them@mail.com'
        assert mime['From'] == 'Me <me@mail.com>'
        assert mime['Subject'] == 'subject'
        assert mime['X-This-That'] == 'Something'
