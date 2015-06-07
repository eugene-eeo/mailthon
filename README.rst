Mailthon
========

**Useful links:** `Documentation`_ | `Issue Tracker`_ | `PyPI Page`_

Mailthon is an email library for Python that aims to be highly
extensible and composable. Mailthon is unicode aware and supports
internationalised headers and email addresses. Also it aims to be
highly transport agnostic, meaning that SMTP can be swapped out
for other transports.

.. code-block:: python

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

Platforms
---------

+-------------+----------------------------------------------------------------------------------+
| **Linux**   | .. image:: https://travis-ci.org/eugene-eeo/mailthon.svg?branch=master           |
|             |     :target: https://travis-ci.org/eugene-eeo/mailthon                           |
+-------------+----------------------------------------------------------------------------------+
| **Windows** | .. image:: https://ci.appveyor.com/api/projects/status/eadeytartlka64a1?svg=true |
|             |     :target: https://ci.appveyor.com/project/eugene-eeo/mailthon                 |
+-------------+----------------------------------------------------------------------------------+
