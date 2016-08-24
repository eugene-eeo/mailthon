Mailthon
========

**Useful links:** `Documentation`_ (outdated) | `Issue Tracker`_ | `PyPI Page`_

Mailthon is an MIT licensed email library for Python that aims to be
highly extensible and composable. Mailthon is unicode aware and supports
internationalised headers and email addresses. Also it aims to be transport
agnostic, meaning that SMTP can be swapped out for other transports::

    >>> from mailthon import postman, email
    >>> p = postman(host='smtp.gmail.com', auth=('username', 'password'))
    >>> r = p.send(email(
            content=u'<p>Hello 世界</p>',
            subject='Hello world',
            sender='John <john@jon.com>',
            receivers=['doe@jon.com'],
        ))
    >>> assert r.ok

.. _Documentation: http://mailthon.readthedocs.org/en/latest/
.. _Issue Tracker: http://github.com/eugene-eeo/mailthon/issues/
.. _PyPI Page: http://pypi.python.org/pypi/Mailthon

.. image:: https://img.shields.io/travis/eugene-eeo/mailthon.svg
    :target: https://travis-ci.org/eugene-eeo/mailthon
.. image:: https://ci.appveyor.com/api/projects/status/eadeytartlka64a1?svg=true
    :target: https://ci.appveyor.com/project/eugene-eeo/mailthon
.. image:: https://img.shields.io/codecov/c/github/eugene-eeo/mailthon.svg
    :target: https://codecov.io/gh/eugene-eeo/mailthon
