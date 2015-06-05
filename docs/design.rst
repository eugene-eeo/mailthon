.. design::

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


No bulk sending
---------------

Usually this feature is expected to be present in libraries.
However Mailthon does not include bulk email sending. This
is not an issue with multiple receipients- that is well
supported but what is meant by bulk sending is the sending
of many emails to many people. This is what it used to
look like::

    postman.send_many([env1, env2, env3])

Where the connection is shared in between the delivery of
all of the three envelopes. That is good when everything
goes well but consider an imaginary situation where there
is an exception raised before the second envelope is sent.
There is no way to inform the user that the second and third
envelopes are not sent. Instead Mailthon leaves this up to
the developer::

    with postman.connection() as conn:
        try:
            respose = postman.deliver(conn, envelope)
            assert response.ok
        except Exception as err:
            handle_exception(err)

One way around this problem is to use something like a cursor
class, where the delivery can be continued arbirtrarily, and
the generator paused whenever an exception occurs such that
the user can resume the sending after it is handled. For
example, something like the following::

    cursor = postman.cursor([env1, env2, env3])
    try:
        cursor.deliver()
    except Exception as err:
        if cursor.sent > 0:
            resolve(err)
            cursor.deliver()
        else:
            raise

Where ``cursor.sent`` is the number of envelopes sent. Once
again this is good and all but presents some resource
handling problems of it's own.
