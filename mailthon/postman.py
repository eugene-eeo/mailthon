from contextlib import contextmanager
from smtplib import SMTP
from .response import SendmailResponse


class Postman:
    transport = SMTP
    response_cls = SendmailResponse

    def __init__(self, server, port, middleware=()):
        self.server = server
        self.port = port
        self.middleware = list(middleware)

    def use(self, preproc):
        self.middleware.append(preproc)

    @contextmanager
    def connection(self):
        conn = self.transport(self.server, self.port)
        try:
            conn.ehlo()
            for item in self.middleware:
                item(conn)
            yield conn
        finally:
            conn.quit()

    def deliver(self, conn, envelope):
        rejected = conn.sendmail(
            envelope.sender,
            envelope.receivers,
            envelope.to_string(),
        )
        return self.response_cls(conn.noop(), rejected)

    def send_many(self, envelopes):
        with self.connection() as conn:
            return [self.deliver(conn, e) for e in envelopes]

    def send(self, envelope):
        return self.send_many([envelope])[0]
