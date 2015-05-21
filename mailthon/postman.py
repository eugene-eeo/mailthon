from contextlib import closing, contextmanager
from smtplib import SMTP
from .response import Response


class Postman:
    response_cls = Response

    def __init__(self, server, port, preprocessors=()):
        self.server = server
        self.port = port
        self.preprocessors = list(preprocessors)

    def use(self, preproc):
        self.preprocessors.append(preproc)

    @contextmanager
    def connection(self):
        conn = SMTP(self.server, self.port)
        with closing(conn):
            conn.ehlo()
            for item in self.preprocessors:
                item(conn)
            yield conn

    def deliver(self, conn, envelope):
        conn.sendmail(
            envelope.sender,
            envelope.receiver,
            envelope.to_string(),
        )
        status, message = conn.noop()
        return self.response_cls(status, message)

    def send(self, envelopes):
        with self.connection() as conn:
            return [self.deliver(e, conn) for e in envelopes]
