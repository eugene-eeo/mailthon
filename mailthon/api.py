from mailthon.attachments import HTML
from mailthon.envelope import Envelope, Stamp
from mailthon.postman import Postman
from mailthon.middleware import TLS, Auth


def html(subject, sender, receiver, content, encoding='utf8'):
    return Envelope(
        Stamp(subject, sender, receiver),
        attachments=[
            HTML(content, encoding=encoding),
        ],
    )


def postman(server, port=587, auth=(None, None), force_tls=False):
    username, password = auth
    return Postman(
        server=server,
        port=port,
        middleware=[
            TLS(force=force_tls),
            Auth(username, password),
        ],
    )
