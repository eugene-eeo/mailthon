from collections import OrderedDict
from email.message import Message as _Message
from email.mime.base import MIMEBase as _Base
from email.mime.text import MIMEText as _Text
from email.mime.image import MIMEImage as _Image


class Headers(OrderedDict):
    def get_all(self, name, failobj=None):
        return [self.get(name, failobj)]


class Message(_Message):
    def __init__(self, *args, **kwargs):
        _Message.__init__(self, *args, **kwargs)
        self._headers = Headers()


class MIMEBase(_Base, Message):
    pass


class MIMEText(_Text, Message):
    pass


class MIMEImage(_Image, Message):
    pass
