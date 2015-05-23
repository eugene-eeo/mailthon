Mailthon
========

MIT licensed library for easy delivery of emails, inspired
by Requests's simple, beautiful API. Mailthon aims to
simplify the delivery of emails and make it a joy to use
as well as being extremely extensible and configurable at
the same time.

.. code-block:: python

    >>> from mailthon import postman, email
    >>> p = postman(host='smtp.google.com', auth=('username', 'password'))
    >>> r = p.send(email(
            content='<p>Hello 世界</p>',
            subject='Hello world',
            sender='John <john@jon.com>',
            receivers=['doe@jon.com'],
        ))
    >>> assert r.ok
