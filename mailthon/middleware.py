class Middleware:
    def __call__(self, conn):
        return


class TLS(Middleware):
    def __init__(self, force=False):
        self.force = force

    def __call__(self, conn):
        if self.force or conn.has_extn('STARTTLS'):
            conn.starttls()
            conn.ehlo()


class Auth(Middleware):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __call__(self, conn):
        conn.login(self.username,
                   self.password)
