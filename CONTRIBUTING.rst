Contributing to Mailthon
========================

Thanks for considering to contribute to Mailthon.

Feedback / Support Questions
----------------------------

- Use the Github Issues system or send me an email if the feedback
  is more personal.

Reporting Issues
----------------

- Include the Python version. Usually this can be done by invoking
  ``python --version``. This is especially important when it comes
  to encoding issues.
- If possible, check that it's already fixed in the latest version
  of the codebase (i.e. the master branch).

Submitting Patches
------------------

- Include regression test(s) if your patch solves a bug. Explain
  how the bug happens and if possible, include version information
  and stack traces. Make sure that the regression test fails without
  your patch. (If only on certain systems).

- Follow PEP 8 to a reasonable extent. Ignore it if it makes the
  code ugly or harder to understand. Readability is more important.

- If you would like to contribute but are not familiar with the
  codebase, look for issues filed under the ``beginner-friendly``
  tag.

Running Tests
#############

The test suite requires pytest and mock::

    $ pip install mock
    $ pip install pytest

Running the test suite is simply::

    $ py.test

Feel free to use pyenv_ to test against many other Pythons. Note
that Travis is already configured to test against the more
frequently used ones when you submit your pull request.

.. _pyenv: https://github.com/yyuu/pyenv
