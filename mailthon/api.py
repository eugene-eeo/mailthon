from mailthon.enclosure import HTML, Attachment
from mailthon.envelope import Envelope, Stamp
from mailthon.postman import Postman
from mailthon.middleware import TLS, Auth
import mailthon.headers as headers


def email(sender=None, receivers=(), cc=(), bcc=(),
          subject=None, content=None, encoding='utf8',
          attachments=()):

    html = [HTML(content, encoding)]
    files = [Attachment(k) for k in attachments]
    return Envelope(
        stamp=Stamp(
            sender=sender,
            receivers=receivers,
            headers=[
                headers.cc(*cc),
                headers.bcc(*bcc),
            ],
        ),
        enclosure=(html + files),
    )


def postman(host, port=587, auth=(None, None),
            force_tls=False, options={}):
    return Postman(
        host=host,
        port=port,
        options=options,
        middlewares=[
            TLS(force_tls=force_tls),
            Auth(username, password),
        ],
    )
