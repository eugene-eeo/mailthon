from re import search
from base64 import b64decode
from email.message import Message


class mimetest:
    def __init__(self, mime):
        self.mime = mime
        assert not mime.defects

    def __getitem__(self, header):
        return self.mime[header]

    @property
    def transfer_encoding(self):
        return self['Content-Transfer-Encoding']

    @property
    def encoding(self):
        return self.mime.get_content_charset(None)

    @property
    def mimetype(self):
        return self.mime.get_content_type()

    @property
    def payload(self):
        payload = self.mime.get_payload().encode(self.encoding or 'ascii')
        if self.transfer_encoding == 'base64':
            return b64decode(payload)
        return payload

    @property
    def parts(self):
        payload = self.mime.get_payload()
        if not isinstance(payload, list):
            raise TypeError
        return [mimetest(k) for k in payload]


def blank():
    return Message()
