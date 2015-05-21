from mailthon.postman import Postman


class MockedSMTP:
    instance = None

    def __init__(self, server, port):
        MockedSMTP.instance = self
        self.server = server
        self.port = port
        self.closed = False
        self.vcr = []

    def __getattr__(self, method):
        if method not in self.__dict__:
            if self.closed:
                raise IOError('SMTP closed')
            return lambda *args: self._record(method, args)
        return self.__dict__[method]

    def _record(self, verb, args=()):
        self.vcr.append((verb, tuple(args)))

    def has_extn(self, extn):
        self._record('has_extn', (extn,))
        return True

    def verbs(self):
        return [verb for verb, args in self.vcr]

    def noop(self):
        self._record('noop')
        return (250, 'message')

    def quit(self):
        self._record('quit')
        self.closed = True

    def sendmail(self, sender, receipients, message):
        self._record('sendmail', [sender, receipients])
        return {}


class MyPostman(Postman):
    transport = MockedSMTP
