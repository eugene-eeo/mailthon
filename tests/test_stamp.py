import pytest
from mailthon.headers import From, To, Subject, Header
from mailthon.stamp import Stamp
from .mimetest import blank


@pytest.fixture
def stamp():
    return Stamp([
        From('Me <me@mail.com>'),
        To('him@mail.com', 'them@mail.com'),
        Subject('subject'),
        Header('X-This-That', 'Something'),
    ])


class TestStamp:
    def test_prepare(self, stamp):
        mime = blank()
        stamp.prepare(mime)

        assert mime['To'] == 'him@mail.com, them@mail.com'
        assert mime['From'] == 'Me <me@mail.com>'
        assert mime['Subject'] == 'subject'
        assert mime['X-This-That'] == 'Something'
