.. _quickstart:

Quickstart
==========

This page gives a good introduction to Mailthon, and assumes
that you already have Mailthon installed. Head over to the
:ref:`installation` section if you do not.

Comparison
----------

A comparison between using the standard library
`smtplib <https://docs.python.org/2/library/smtplib.html>`_ module and
Mailthon::

    from smtplib import SMTP
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage

    text = MIMEText('<html><p>Hi!</p></html>', 'html')
    image = MIMEImage(open('cats.gif', 'rb').read())

    mime = MIMEMultipart()
    mime['Sender'] = 'Me <me@mail.com>'
    mime['To'] = 'Them <them@mail.com>'
    mime.attach(text)
    mime.attach(image)

    smtp = SMTP(host='smtp.server.com', port=587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('username', 'password')
    smtp.sendmail(
        mime['Sender'],
        mime['To'],
        mime.as_string()
    )
    smtp.quit()

Using Mailthon all this cruft is reduced::

    from mailthon import postman, email
    
    smtp = postman(host='smtp.server.com', port=587, auth=('username', 'password'))
    smtp.send(email(
        sender='Me <me@mail.com>',
        receivers=['Them <them@mail.com>'],
        content='<html><p>Hi!</p></html>',
        attachments=[
            'cats.gif',
        ]
    ))

Quoting Kenneth Reitz, "things shouldn't be like that,
not in Python.".


Creating an Email
-----------------

Creating a minimal email looks like the following::

    from mailthon.envelope import Envelope
    from mailthon.enclosure import PlainText

    envelope = Envelope( 
        headers={
            'Sender': 'sender <username@mail.com>',
            'To': 'receiver@mail.com',
            'Subject': 'Hello World!',
        },
        enclosure=[
            PlainText('Hi!'),
        ]
    )

What did the code do?

1. First a new :class:`~mailthon.envelope.Envelope` instance
   is created. An Envelope is like a real life envelope- it
   contains stamps (headers) and an enclosure.
2. The Envelope is created with the bare minimum- the
   ``Sender``, ``To``, and ``Subject`` headers. This time
   we make them manually, but we'll see how we can create
   them easily in the next section. Mailthon knows how to
   automatically convert the values to Unicode and vice
   versa when sending the email.
3. A :class:`~mailthon.enclosure.PlainText` instance is made
   which represents plain-text content. It has the mimetype
   of ``text/plain``, and a UTF8 encoding by default.

There is a convenience function called :func:`~mailthon.email`
module that enables us to do what we did in fewer lines of
code::

    from mailthon import email

    envelope = email(
        sender='sender <username@mail.com>',
        receivers=['receiver@mail.com'],
        subject='Hello World!',
        content='Hi!',
    )

However take note that the :func:`~mailthon.email`
function makes an email with a :class:`~mailthon.enclosure.HTML`
enclosure, not the plaintext one like what we've just created.
An alternative to building the headers by hand is to use the
mailthon.headers module::

    import mailthon.headers as headers

    Envelope(
        headers=[
            headers.sender('sender <username@mail.com>'),
            headers.to('receiver@mail.com'),
            headers.subject('Hello World!'),
        ],
        enclosure=[],
    )


Creating a Postman
------------------

Mailthon uses rather quirky real-life names to represent
abstract email concepts. What better name for something
that delivers an envelope than a postman? To create a
postman that is configured for a GMail server::

    from mailthon.postman import Postman
    from mailthon.middleware import TLS, Auth

    postman = Postman(
        host='mail.google.com',
        port=587,
        middlewares=[
            TLS(force=True),
            Auth(username='USERNAME', password='PASSWORD')
        ],
    )

(Substitute ``USERNAME`` and ``PASSWORD`` with your credentials,
obtained from the `Authorizing applications & sites page <https://www.google.com/accounts/IssuedAuthSubTokens?hide_authsub=1>`_.)
So what did we just do?

1. We created a :class:`~mailthon.postman.Postman` instance.
   A Postman handles the sending of emails via some transport,
   usually that defaults to SMTP. The Postman is created with
   the correct host and port arguments.
2. We configured the :class:`~mailthon.middleware.Auth`
   and :class:`~mailthon.middleware.TLS` middleware. They provide
   authentication and TLS support, respectively. We also forced
   TLS because we know that the GMail SMTP server only allows
   us to login if we have TLS enabled (which is also the reason
   why it is placed before the authentication middleware).

There is again, a simpler function for handling that in the form
of the :func:`~mailthon.postman` function::

    from mailthon import postman as postman_

    postman = postman_(
        host='mail.google.com',
        port=587,
        force_tls=True,
        auth=('USERNAME', 'PASSWORD'),
    )

Sending an Envelope
-------------------

After creating an envelope and a postman, we can then send the
envelope to the receivers using the :meth:`~mailthon.postman.Postman.send`
method::

    response = postman.send(envelope)

Which returns the result of the sending the envelope- whether the
server accepted it, whether everything went OK, etc. You can access
the response values::

    print(response.message)
    print(response.status_code)

    if response.ok:
        print("OK! :)")

You might want to continue reading about Mailthon's architecture
in the :ref:`indepth`, or dive into the internals in the :ref:`api`
section.
