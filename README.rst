Mailthon
========

.. image:: https://travis-ci.org/eugene-eeo/mailthon.svg?branch=master
    :target: https://travis-ci.org/eugene-eeo/mailthon

.. image:: https://ci.appveyor.com/api/projects/status/eadeytartlka64a1?svg=true
    :target: https://ci.appveyor.com/project/eugene-eeo/mailthon

MIT licensed library for easy delivery of emails, inspired
by Requests's simple, beautiful API. Mailthon aims to
simplify the delivery of emails and make it a joy to use
as well as being extremely extensible and configurable at
the same time.

.. code-block:: python

    >>> from mailthon import postman, email
    >>> p = postman(host='smtp.gmail.com', auth=('username', 'password'))
    >>> r = p.send(email(
            content='<p>Hello 世界</p>',
            subject='Hello world',
            sender='John <john@jon.com>',
            receivers=['doe@jon.com'],
        ))
    >>> assert r.ok

The library is still in rapid development and the edges
are being ironed out. Feel free to raise issues/ping me
if you want to give feedback. Also, you can always make
pull requests if you prefer expressing yourself in code.
