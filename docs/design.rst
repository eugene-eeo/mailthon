.. _design:

Design Decisions
================

This section is meant for those who are curious about why
certain parts of Mailthon is designed the way it is, and
should give you some idea on decisions which may seem quite
weird at first.

The Postman Object
------------------

Usually most users would expect something like the following,
where the envelope object itself knows how to send itself.
After all, it's an envelope, right? Before we start throwing
buzzwords around consider a hypothetical Mailthon which looks
like the following::

    from hypmail.envelope import Envelope

    Envelope(...).deliver(
        host='smtp.google.com',
        port=587,
        auth=('username', 'password'),
    )

Which, while convenient in some situations, just breaks down
whenever you want to do something more complex. For example
consider the following situations:

1. You want to send the same envelope using different servers
   or transport. Where should it go? I suppose you could do
   something like the following where the method calls are
   just replayed on each envelope::

        env = Envelope(...)
        for server in servers: 
            preparer[server](env)
            env.deliver(**options[server])

   But then again you run into issues like "did I change this
   attribute before I delivered it?" Which ultimately leads to
   hard to find, hard to debug errors.
2. You want to send multiple envelopes but using the same
   server configuration and middleware. Once again this can
   be solved via some preparation functions::

        for env in envelopes:
            prepare(env)
            env.deliver(**options)

   Once again this leads to conceptual issues and practical
   issues. For example it is cumbersome to keep track of
   some configuration just to pass it to a method. Also
   it is extremely unweildly to have a giant Envelope class
   that does everything.

Unicode Headers
---------------

This design decision is in fact inspired by Werkzeug. Basically,
SMTP allows you to specify headers of different encodings, e.g.
UTF-8 headers for chinese characters in the subject field. While
the :class:`~email.message.Message` objects allow you to pass in
unicode or byte strings, or even :class:`~email.header.Header`
objects as the header values- Mailthon chooses to pass in Unicode
values.

The background is simple- so that users writing special headers
do not need to worry about weird encoding problems that do not
usually show up until the time where you least expect them to.
Thus the :class:`~mailthon.helpers.UnicodeDict` class was born::

    >>> from mailthon.helpers import UnicodeDict
    >>> d = UnicodeDict()
    >>> d['uni'] = u'unicode'
    >>> d['uni']
    u'unicode'
    >>> d['key'] = b'value'
    >>> d['key']
    u'value'

Which automatically tries to decode bytes values into Unicode
strings. This makes development of Headers very painless; you
can pass in whatever value in Unicode- they will all look the
same and thus can be very easily programmed against. Also it
makes passing in a special ``mail_from`` parameter to the
:class:`~mailthon.envelope.Envelope`` class simpler; you do
not need to worry about encoding since the :class:`~mailthon.postman.Postman`
object encodes it for you behind the scenes, using the
:func:`~mailthon.helpers.stringify_address` function.
