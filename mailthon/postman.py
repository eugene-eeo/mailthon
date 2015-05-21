from contextlib import closing, contextmanager
from smtplib import SMTP


class Postman:
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

    def send(self, envelope):
        message = envelope.to_string()
        with self.connection() as conn:
            conn.sendmail(envelope.sender,
                          envelope.receiver,
                          message)
