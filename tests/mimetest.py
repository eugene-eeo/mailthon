from base64 import b64decode
from email import message_from_string
from email.message import Message


class mimetest:
    def __init__(self, mime):
        string = mime if isinstance(mime, str) else mime.as_string()
        self.mime = message_from_string(string)

    def __getitem__(self, header):
        return self.mime[header]

    @property
    def transfer_encoding(self):
        return self['Content-Transfer-Encoding']

    @property
    def encoding(self):
        return self['Content-Encoding']

    @property
    def mimetype(self):
        return self['Content-Type'].split()[0].strip(';')

    @property
    def payload(self):
        payload = self.mime.get_payload()
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
