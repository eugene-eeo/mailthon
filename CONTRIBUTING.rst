Contribution Guidelines
=======================

Whether you are submitting new features, filing issues, discussing
improvements or giving feedback about the library, all are welcome!
To get started:

1. Check for related issues or open a fresh one to start discussion
   around an idea or a bug.
2. Fork the `repository <https://github.com/eugen-eeo/mailthon>`_,
   create a new branch off `master` and make your changes.
3. Write a regression test which shows that the bug was fixed or the
   feature works as expected. If it's a bug, try to make sure the
   tests fail without your changes. Tests can be ran via the
   ``py.test`` command.
4. Submit a pull request!

Philosophy
**********

Mailthon aims to be easy to use while being very extensible at
the same time. Therefore two values needed to be upholded- the
simplicity and elegance of the code. Sometimes they will contradict
one another; in that case prefer the approach with fewer magic,
in fact don't try to include magic if possible.

Code Conventions
****************

Generally the Mailthon codebase follows rules dictated by
`PEP 8 <http://legacy.python.org/dev/peps/pep-0008/>`_. Sometimes
following PEP8 makes the code uglier. In that case feel free to
break from the rules if it makes your code more understandable.
A minor exception concerning docstrings:

When multiline docstrings are used, keep the triple quotes on
their own line and do not put a separate newline after it if
it is not necessary. This convention is used by Flask et al.

.. code-block:: python

    def function():
        """
        Documentation
        """
        # implementation
        return value
