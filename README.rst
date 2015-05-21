Mailthon
========

MIT licensed library for easy delivery of emails, inspired
by Requests's simple, beautiful API.

.. code-block:: python

    >>> from mailthon import postman, html
    >>> p = postman(server='smtp.google.com', auth=('username', 'password'))
    >>> e = html(
            content='<p>hi!</p>',
            subject='Hello world',
            sender=('John', 'john@jon.com'),
            receiver=('Doe', 'doe@jon.com'),
        )
    >>> r = p.send([e])
    >>> assert [res.ok for res in r]
