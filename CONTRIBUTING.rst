How to contribute to Mailthon
=============================

Thanks for considering to contribute to Mailthon.

Reporting Issues
----------------

 - Include the Python version, as well as the Mailthon version.
   The former is especially important if the issue is encoding
   related.
 - If possible, check if it was already fixed in the latest
   source code.

Submitting Patches
------------------

 - Include tests if your patch solves a bug. Explain how to bug
   happens and include a stack trace if possible. Make sure the
   regression test fails without your changes (if only on
   certain systems).
 - Follow PEP8 to a reasonable extent- but ignore it if it makes
   the code uglier/harder to grok.

Running tests
#############

The test suite requires pytest and mock (for the SMTP server).
You can install them with::

    $ pip install mock
    $ pip install pytest

Running the test suite is simply::

    $ py.test

You can also use pyenv_ to test against many other Python versions,
but Travis CI is configured to test against all of them when you
submit your pull request.

.. _pyenv: https://github.com/yyuu/pyenv
