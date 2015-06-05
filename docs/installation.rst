.. _installation:

Installation
============

Mailthon does not have any external dependencies apart from
the Python standard library. Mailthon is however, only
tested against Python 2.6 or newer, so make sure you have
an up-to-date Python installation. Mailthon also supports
Python 3.

.. _pip:

Installing a stable version
---------------------------

Usually you want to install the latest stable version. Pulling
the package from PIP is what you want. I recommend using a
`virtualenv`_ but that is not required to install Mailthon::

    $ pip install Mailthon

Before you do that however you should check if you have PIP
installed, which is a package manager for python. If you
don't, just download the `get-pip.py`_ script and run it.

.. _edge:

Living on the edge
------------------

If you want to work on Mailthon or download the latest
version, it is recommended that clone from the git
repository, because you can always check out the latest
version of the codebase and keep your local copy in
sync with the latest goodies (Virtualenv is recommended)::

    $ git clone http://github.com/eugene-eeo/mailthon.git
    $ cd mailthon
    $ virtualenv venv
    New python executable in venv/bin/python
    Installing setuptools, pip..............done.
    $ . venv/bin/activate
    $ python setup.py develop

This will pull in the latest codebase and activate the
git head as the current version inside the virtualenv.
All you have to do is run ``git pull origin`` to update
to the latest version.

.. _virtualenv: https://virtualenv.pypa.io/en/latest/
.. _get-pip.py: https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
