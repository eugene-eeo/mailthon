from re import search
from base64 import b64decode
from email.message import Message


class mimetest:
    def __init__(self, mime):
        self.mime = mime

    def __getitem__(self, header):
        return self.mime[header]

    @property
    def transfer_encoding(self):
        return self['Content-Transfer-Encoding']

    @property
    def encoding(self):
        ctype = self['Content-Type'].split()
        if len(ctype) >= 2:
            match = search('charset="(.+?)"', ctype[1])
            if match:
                return match.group(1)

    @property
    def mimetype(self):
        return self['Content-Type'].split()[0].strip(';')

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
