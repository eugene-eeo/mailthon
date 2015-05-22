from base64 import b64decode
from email import message_from_string


class mimetest:
    def __init__(self, mime, rebuild=True):
        if rebuild:
            mime = message_from_string(mime.as_string())
        self.mime = mime

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
